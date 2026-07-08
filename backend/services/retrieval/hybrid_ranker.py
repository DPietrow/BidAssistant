class HybridRanker:


    def normalize_semantic(
        self,
        score
    ):

        """
        Convert cosine similarity range.

        Typical embedding range:
        .45 = weak
        .70 = strong

        Map into 0-1 relevance.
        """

        if score <= 0:
            return 0


        normalized = (
            score - 0.45
        ) / (
            0.75 - 0.45
        )


        return max(
            0,
            min(
                normalized,
                1
            )
        )



    def normalize_keyword(
        self,
        score
    ):

        """
        PostgreSQL ts_rank
        usually ranges 0-1.

        Keep bounded.
        """

        return max(
            0,
            min(
                score,
                1
            )
        )



    def fuse(
        self,
        semantic_results,
        keyword_results,
        limit=10
    ):


        results = {}



        #
        # Semantic results
        #

        for item in semantic_results:


            contract_id = item["contract_id"]


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


                "semantic_score":
                    self.normalize_semantic(
                        item.get(
                            "semantic_score",
                            0
                        )
                    ),


                "raw_semantic_score":
                    item.get(
                        "semantic_score",
                        0
                    ),


                "keyword_score":
                    0,

                "keyword_match_type": 
                 item.get(
                    "keyword_match_type"
                  ),

                "match":

                    {
                        "chunk_id":
                            item.get(
                                "chunk_id"
                            ),

                        "chunk_text":
                            item.get(
                                "chunk_text"
                            )
                    }


            }



        #
        # Keyword results
        #

        for item in keyword_results:


            contract_id = item["contract_id"]


            keyword_score = self.normalize_keyword(
                item["keyword_score"]
            )


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


                    "semantic_score":
                        0,


                    "raw_semantic_score":
                        0,


                    "keyword_score":
                        keyword_score,

                    "keyword_match_type":
                        item.get(
                            "keyword_match_type",
                            "keyword"
                        ),

                    "match":
                        None

                }


            else:


                results[contract_id]["keyword_score"] = keyword_score

                results[contract_id]["keyword_match_type"] = (
                    item.get(
                        "keyword_match_type"
                    )
                )



        ranked = []



        for contract in results.values():


            semantic = contract["semantic_score"]

            keyword = contract["keyword_score"]



            #
            # Exact identifier
            #

            if keyword >= 0.95:


                fusion_score = 1.0

                match_type = (
                    "exact_identifier"
                )



            #
            # Both systems agree
            #

            elif semantic > 0 and keyword > 0:


                fusion_score = (

                    semantic * 0.55

                    +

                    keyword * 0.45

                )

                match_type = "hybrid"



            #
            # Semantic only
            #

            elif semantic > 0:


                fusion_score = (

                    semantic * 0.85

                )

                match_type = "semantic"



            #
            # Keyword only
            #

            else:

                #
                # Heavy penalty
                # prevents noisy keyword results
                #

                keyword_type = contract.get(
                    "keyword_match_type"
                )


                #
                # Strong metadata matches
                #

                if keyword_type == "title_match":
                
                    fusion_score = keyword * 0.90


                elif keyword_type == "naics_match":
                
                    fusion_score = keyword * 0.70


                elif keyword_type == "full_text":
                
                    fusion_score = keyword * 0.45


                else:
                
                    fusion_score = keyword * 0.50



                match_type = keyword_type or "keyword"



            contract["fusion_score"] = round(
                fusion_score,
                4
            )


            contract["match_type"] = match_type


            ranked.append(contract)



        ranked.sort(

            key=lambda x:
                x["fusion_score"],

            reverse=True

        )


        return ranked[:limit]



hybrid_ranker = HybridRanker()