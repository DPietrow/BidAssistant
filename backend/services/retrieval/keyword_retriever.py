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

                c.url,


                CASE


                    -- Exact identifiers

                    WHEN c.sam_id = :query
                    THEN 1.0


                    WHEN c.solicitation_number = :query
                    THEN 1.0


                    WHEN c.psc_code = :query
                    THEN 0.95



                    -- Metadata boosts

                    WHEN c.title ILIKE '%' || :query || '%'
                    THEN 0.85


                    WHEN c.naics = :query
                    THEN 0.80



                    -- Full text

                    ELSE ts_rank_cd(

                        c.search_vector,

                        websearch_to_tsquery(

                            'english',

                            :query

                        )

                    )


                END AS keyword_score,



                CASE


                    WHEN c.sam_id = :query

                    OR c.solicitation_number = :query

                    OR c.psc_code = :query

                    THEN 'exact_identifier'



                    WHEN c.title ILIKE '%' || :query || '%'

                    THEN 'title_match'



                    WHEN c.naics = :query

                    THEN 'naics_match'



                    ELSE 'full_text'


                END AS keyword_match_type



            FROM contracts c



            WHERE


                c.sam_id = :query

                OR c.solicitation_number = :query

                OR c.psc_code = :query


                OR c.title ILIKE '%' || :query || '%'


                OR c.naics = :query


                OR c.search_vector @@ websearch_to_tsquery(

                    'english',

                    :query

                )


        )



        SELECT *

        FROM ranked



        WHERE keyword_score > 0



        ORDER BY keyword_score DESC



        LIMIT :limit


        """
        )


        rows = db.session.execute(
            sql,
            {
                "query": query.strip(),

                "limit": limit
            }
        )



        results = []



        for row in rows:


            print(
                row._mapping
            )


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


                "keyword_score":
                    float(
                        row.keyword_score
                    ),


                "keyword_match_type":
                    row.keyword_match_type

            })


        return results



keyword_retriever = KeywordRetriever()