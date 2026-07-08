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


                "match_type":
                    self.get_match_type(
                        semantic_score,
                        keyword_score
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
                        result.get("naics")

                },


                "match": {

                    "chunk_id":
                        match.get("chunk_id")
                        if match
                        else None,


                    "matched_text":
                         match.get("chunk_text")
                         if match
                         else (
                             f"Exact identifier match: "
                             f"{result['sam_id']}"
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
                        )

                }

            })


        return response



    def get_match_type(
        self,
        semantic_score,
        keyword_score
    ):


        #
        # Exact SAM ID / solicitation match
        #

        if keyword_score >= 0.95:

            return "exact_identifier"



        #
        # Both retrieval systems agree
        #

        if (
            semantic_score > 0
            and
            keyword_score > 0
        ):

            return "hybrid"



        #
        # Embedding similarity only
        #

        if semantic_score > 0:

            return "semantic"



        #
        # PostgreSQL full text only
        #

        if keyword_score > 0:

            return "keyword"



        return "unknown"



    def get_confidence(
        self,
        score
    ):

        if score >= 0.70:
            return "high"


        if score >= 0.50:
            return "medium"


        if score >= 0.35:
            return "low"


        return "very_low"



search_service = SearchService()