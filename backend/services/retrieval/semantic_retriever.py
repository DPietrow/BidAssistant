from sqlalchemy import text

from database import db


class SemanticRetriever:

    def search(
        self,
        query_vector,
        filters=None,
        limit=50,
        threshold=0.45
    ):

        filters = filters or {}

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

                    c.notice_type,

                    c.set_aside,

                    c.posted_date,

                    c.close_date,

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

                WHERE

                    (:agency IS NULL
                        OR c.agency = :agency)

                AND (:naics IS NULL
                        OR c.naics = :naics)

                AND (:notice_type IS NULL
                        OR c.notice_type = :notice_type)

                AND (:set_aside IS NULL
                        OR c.set_aside = :set_aside)

                AND (:posted_after IS NULL
                        OR c.posted_date >= :posted_after)

                AND (:close_before IS NULL
                        OR c.close_date <= :close_before)

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

        params = {

            "embedding": str(query_vector),

            "threshold": threshold,

            "limit": limit,

            "agency": filters.get("agency"),

            "naics": filters.get("naics"),

            "notice_type": filters.get("notice_type"),

            "set_aside": filters.get("set_aside"),

            "posted_after": filters.get("posted_after"),

            "close_before": filters.get("close_before")

        }

        rows = db.session.execute(
            sql,
            params
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

                "notice_type":
                    row.notice_type,

                "set_aside":
                    row.set_aside,

                "posted_date":
                    row.posted_date,

                "close_date":
                    row.close_date,

                "url":
                    row.url,

                "chunk_id":
                    row.chunk_id,

                "chunk_text":
                    row.chunk_text,

                "semantic_score":
                    float(row.semantic_score)

            })

        return results


semantic_retriever = SemanticRetriever()