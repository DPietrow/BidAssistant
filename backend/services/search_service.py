from services.embedding_service import embedding_service

from services.retrieval.semantic_retriever import (
    semantic_retriever
)

from services.retrieval.keyword_retriever import (
    keyword_retriever
)

from services.retrieval.hybrid_ranker import (
    hybrid_ranker
)

from services.retrieval.crossencoder_ranker import (
    cross_encoder_ranker
)

from services.llm_answer_generator import (
    answer_generator
)

class SearchService:


    def search(
        self,
        query,
        limit=10
    ):

        query_vector = embedding_service.embed_query(
            query
        )


        semantic_results = semantic_retriever.search(
            query_vector=query_vector,
            limit=limit
        )


        keyword_results = keyword_retriever.search(
            query=query,
            limit=limit
        )


        fused = hybrid_ranker.fuse(
            semantic_results,
            keyword_results,
            limit
        )


        response = []


        for rank, result in enumerate(
            fused[:limit],
            start=1
        ):


            match = result.get(
                "match"
            )


            semantic_score = float(
                result.get(
                    "semantic_score",
                    0
                )
            )


            keyword_score = float(
                result.get(
                    "keyword_score",
                    0
                )
            )


            response.append({

                "rank": rank,

                "retrieval_score":
                    round(
                        result["fusion_score"],
                        5
                    ),

                "semantic_score":
                    round(
                        semantic_score,
                        4
                    ),

                "keyword_score":
                    round(
                        keyword_score,
                        4
                    ),

                "match_type":
                    result.get(
                        "match_type"
                    ),

                "keyword_match_type":
                     result.get(
                         "keyword_match_type"
                     ),
                    
                "confidence":
                    self.get_confidence(
                        result["fusion_score"]
                    ),


                "contract": {

                    "contract_id":
                        result["contract_id"],

                    "sam_id":
                        result["sam_id"],

                    "title":
                        result["title"],

                    "agency":
                        result["agency"],

                    "naics":
                        result.get("naics"),

                    "url":
                        result.get("url")

                },


                "match": {

                    "chunk_id":
                        match.get("chunk_id")
                        if match
                        else None,


                     "matched_text":
                         match.get("chunk_text")
                         if match
                         else self.get_keyword_match_text(
                             result
                         )

                }

            })

        # Cross encode
        response = cross_encoder_ranker.rerank(
            query=query,
            results=response,
            top_k=5
        )

        for rank, item in enumerate(
            response,
            start=1
        ):
            item["rank"] = rank

        answer = answer_generator.generate(
            query=query,
            results=response
        )

        citations = []


        for item in response:
        
        
            citations.append({
            
                "title":
                    item["contract"]["title"],

                "agency":
                    item["contract"]["agency"],

                "sam_id":
                    item["contract"]["sam_id"],

                "url":
                    item["contract"].get(
                        "url"
                    )

            })

        return {

            "answer":
                answer,

            "citations":
                citations,

            "results":
                response

        }

        


    def get_keyword_match_text(
        self,
        result
    ):

        match_type = result.get(
            "keyword_match_type"
        )


        if match_type == "exact_identifier":

            return (
                f"Exact identifier match: "
                f"{result['sam_id']}"
            )


        if match_type == "title_match":

            return (
                f"Title match: "
                f"{result['title']}"
            )


        if match_type == "naics_match":

            return (
                f"NAICS match: "
                f"{result.get('naics')}"
            )


        if match_type == "full_text":

            return (
                "Full text keyword match"
            )


        return None



    def get_confidence(self, score, match_type=None):

        if match_type == "hybrid":

            if score >= .80:
                return "very_high"

            return "high"


        if match_type == "exact_identifier":

            return "very_high"


        if match_type in [
            "title_match",
            "naics_match"
        ]:

            if score >= .75:
                return "high"

            return "medium"


        if score >= .70:
            return "medium"


        if score >= .45:
            return "low"


        return "very_low"



search_service = SearchService()