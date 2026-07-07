from sqlalchemy import text

from database import db

from models import (
    Contract,
    ContractChunk,
    ContractEmbedding
)

from services.embedding_service import embedding_service



class SearchService:


    def search(
        self,
        query,
        limit=10
    ):

        #
        # 1. Embed user query
        #

        query_vector = (
            embedding_service
            .embed_query(query)
        )


        #
        # 2. Vector similarity search
        #

        sql = text(
            """
            SELECT

                ce.chunk_id,

                cc.chunk_text,

                c.id AS contract_id,

                c.sam_id,

                c.title,

                c.agency,

                c.naics,

                1 - (
                    ce.embedding <=> :embedding
                ) AS similarity


            FROM contract_embeddings ce


            JOIN contract_chunks cc

            ON ce.chunk_id = cc.id


            JOIN contracts c

            ON cc.contract_id = c.id


            ORDER BY

                ce.embedding <=> :embedding


            LIMIT :limit

            """
        )


        rows = db.session.execute(
            sql,
            {
                "embedding": query_vector,
                "limit": limit
            }
        )



        results = []


        for row in rows:

            results.append({

                "contract_id": row.contract_id,

                "sam_id": row.sam_id,

                "title": row.title,

                "agency": row.agency,

                "naics": row.naics,

                "chunk_id": row.chunk_id,

                "chunk_text": row.chunk_text,

                "similarity": round(
                    float(row.similarity),
                    4
                )

            })


        return results



search_service = SearchService()