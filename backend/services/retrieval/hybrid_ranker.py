class HybridRanker:


    def fuse(
        self,
        semantic_results,
        keyword_results,
        limit=10
    ):

        results = {}


        #
        # Semantic retrieval
        #

        for item in semantic_results:

            contract_id = item["contract_id"]


            results[contract_id] = {

                "contract_id": contract_id,

                "sam_id": item["sam_id"],

                "title": item["title"],

                "agency": item["agency"],

                "naics": item.get("naics"),


                "semantic_score":
                    item.get(
                        "semantic_score",
                        0
                    ),

                "keyword_score": 0,


                "match": {

                    "chunk_id":
                        item.get("chunk_id"),

                    "chunk_text":
                        item.get("chunk_text")

                }

            }



        #
        # Keyword retrieval
        #

        for item in keyword_results:


            contract_id = item["contract_id"]


            if contract_id not in results:


                results[contract_id] = {

                    "contract_id":
                        contract_id,

                    "sam_id":
                        item["sam_id"],

                    "title":
                        item["title"],

                    "agency":
                        item["agency"],

                    "naics":
                        item.get("naics"),


                    "semantic_score": 0,

                    "keyword_score":
                        item["keyword_score"],

                    "match": None

                }


            else:

                results[contract_id]["keyword_score"] = (
                    item["keyword_score"]
                )



        #
        # Calculate fusion score
        #

        ranked = []


        for contract in results.values():


            semantic = contract["semantic_score"]

            keyword = contract["keyword_score"]


            #
            # Exact identifier match
            #

            if keyword >= 0.95:

                fusion_score = keyword


            elif semantic > 0:

                fusion_score = (
                    semantic * 0.7
                    +
                    keyword * 0.3
                )

            else:
            
                fusion_score = keyword * 0.15



            contract["fusion_score"] = round(
                fusion_score,
                4
            )


            ranked.append(contract)



        #
        # Sort
        #

        ranked.sort(

            key=lambda x:
                x["fusion_score"],

            reverse=True

        )


        return ranked[:limit]



hybrid_ranker = HybridRanker()