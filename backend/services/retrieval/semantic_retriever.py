from sqlalchemy import text

from database import db


class SemanticRetriever:


    def search(
        self,
        query_vector,
        limit=50,
        threshold=0.45
    ):


        sql = text(
            """
            WITH ranked_chunks AS (

                SELECT

                    ce.chunk_id,

                    cc.chunk_text,

                    c.id AS contract_id,

                    c.sam_id,

                    c.title,

                    c.agency,

                    c.naics,

                    c.url,


                    1 - (
                        ce.embedding <=> CAST(:embedding AS vector)
                    ) AS semantic_score,


                    ROW_NUMBER() OVER(

                        PARTITION BY c.id

                        ORDER BY
                            ce.embedding <=> CAST(:embedding AS vector)

                    ) AS contract_rank


                FROM contract_embeddings ce


                JOIN contract_chunks cc

                ON ce.chunk_id = cc.id


                JOIN contracts c

                ON cc.contract_id = c.id

            )


            SELECT *

            FROM ranked_chunks


            WHERE

                contract_rank = 1

            AND

                semantic_score > :threshold


            ORDER BY

                semantic_score DESC


            LIMIT :limit

            """
        )


        rows = db.session.execute(
            sql,
            {
                "embedding": str(query_vector),

                "threshold": threshold,

                "limit": limit
            }
        )


        results = []


        for row in rows:


            results.append({

                "contract_id":
                    row.contract_id,


                "sam_id":
                    row.sam_id,


                "title":
                    row.title,


                "agency":
                    row.agency,


                "naics":
                    row.naics,

                "url":
                    row.url,


                "chunk_id":
                    row.chunk_id,


                "chunk_text":
                    row.chunk_text,


                "semantic_score":
                    float(
                        row.semantic_score
                    )

            })


        return results



semantic_retriever = SemanticRetriever()