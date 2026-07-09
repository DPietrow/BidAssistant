from sentence_transformers import CrossEncoder



class CrossEncoderRanker:


    def __init__(self):

        self.model = CrossEncoder(
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )



    def normalize_score(
        self,
        score
    ):

        """
        Convert raw cross encoder logits
        into 0-1 range.
        """

        score = float(score)


        normalized = (
            score + 10
        ) / (
            20
        )


        return max(
            0,
            min(
                normalized,
                1
            )
        )



    def rerank(
        self,
        query,
        results,
        top_k=5
    ):


        if not results:

            return []



        pairs = []


        for result in results:


            evidence = (
                result["match"]["matched_text"]
                or
                result["contract"]["title"]
            )


            pairs.append(

                (
                    query,
                    evidence
                )

            )



        scores = self.model.predict(
            pairs
        )



        for result, score in zip(
            results,
            scores
        ):


            result["cross_encoder_raw_score"] = float(
                score
            )


            result["cross_encoder_score"] = round(

                self.normalize_score(
                    score
                ),

                4

            )



        results.sort(

            key=lambda x:
                x["cross_encoder_score"],

            reverse=True

        )



        return results[:top_k]



cross_encoder_ranker = CrossEncoderRanker()