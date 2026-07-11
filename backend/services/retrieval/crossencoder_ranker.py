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
        Convert raw CrossEncoder logits
        into a 0-1 score.
        """

        score = float(score)

        normalized = (score + 10) / 20

        return max(
            0,
            min(normalized, 1)
        )

    def rerank(
        self,
        query,
        results,
        intent=None,
        top_k=5
    ):

        if not results:
            return []

        pairs = []

        for result in results:

            contract = result["contract"]

            evidence = (
                result["match"].get("matched_text")
                or contract.get("title", "")
            )

            #
            # Build a richer document for the CrossEncoder.
            #
            document = f"""
Title:
{contract.get("title", "")}

Agency:
{contract.get("agency", "")}

NAICS:
{contract.get("naics", "")}

Evidence:
{evidence}
""".strip()

            #
            # Build the query side.
            #
            if intent:

                query_text = f"""
Search Query:
{query}

Mission:
{intent}
""".strip()

            else:

                query_text = query

            pairs.append(
                (
                    query_text,
                    document
                )
            )

        scores = self.model.predict(pairs)

        for result, score in zip(results, scores):

            normalized = self.normalize_score(score)

            result["cross_encoder_raw_score"] = float(score)

            result["cross_encoder_score"] = round(
                normalized,
                4
            )

            #
            # Athena-friendly score (0-100)
            #
            result["athena_score"] = int(
                round(normalized * 100)
            )

        results.sort(
            key=lambda x: x["cross_encoder_score"],
            reverse=True
        )

        return results[:top_k]


cross_encoder_ranker = CrossEncoderRanker()