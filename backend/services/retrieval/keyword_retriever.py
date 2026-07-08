from sqlalchemy import text

from database import db



class KeywordRetriever:


    def search(
        self,
        query,
        limit=10
    ):


        sql = text(
        """
        WITH ranked AS (

            SELECT

                c.id AS contract_id,

                c.sam_id,

                c.title,

                c.agency,

                c.naics,


                CASE

                    WHEN c.sam_id ILIKE :exact
                    THEN 1.0


                    WHEN c.solicitation_number ILIKE :exact
                    THEN 1.0


                    WHEN c.psc_code ILIKE :exact
                    THEN 0.9


                    ELSE ts_rank(
                        c.search_vector,
                        websearch_to_tsquery(
                            'english',
                            :query
                        )
                    )

                END AS keyword_score


            FROM contracts c


            WHERE


                c.sam_id ILIKE :exact

                OR

                c.solicitation_number ILIKE :exact

                OR

                c.search_vector @@ websearch_to_tsquery(
                    'english',
                    :query
                )


        )


        SELECT *

        FROM ranked

        ORDER BY keyword_score DESC

        LIMIT :limit

        """
        )


        rows = db.session.execute(
            sql,
            {
                "query": query,

                "exact": f"%{query}%",

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

                "keyword_score":
                    float(row.keyword_score)

            })


        return results



keyword_retriever = KeywordRetriever()