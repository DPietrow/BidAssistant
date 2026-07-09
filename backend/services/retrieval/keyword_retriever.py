from sqlalchemy import text

from database import db


class KeywordRetriever:

    def search(
        self,
        query,
        filters=None,
        limit=10
    ):

        filters = filters or {}

        sql = text(
        """

        WITH ranked AS (

            SELECT

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


                CASE

                    --
                    -- Exact identifiers
                    --

                    WHEN c.sam_id = :query
                    THEN 1.0

                    WHEN c.solicitation_number = :query
                    THEN 1.0

                    WHEN c.psc_code = :query
                    THEN 0.95


                    --
                    -- Metadata
                    --

                    WHEN c.title ILIKE '%' || :query || '%'
                    THEN 0.85

                    WHEN c.naics = :query
                    THEN 0.80


                    --
                    -- Full text
                    --

                    ELSE ts_rank_cd(

                        c.search_vector,

                        websearch_to_tsquery(
                            'english',
                            :query
                        )

                    )

                END AS keyword_score,


                CASE

                    WHEN
                        c.sam_id = :query
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

            (

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

            AND

                (:agency IS NULL
                    OR c.agency = :agency)

            AND

                (:naics_filter IS NULL
                    OR c.naics = :naics_filter)

            AND

                (:notice_type IS NULL
                    OR c.notice_type = :notice_type)

            AND

                (:set_aside IS NULL
                    OR c.set_aside = :set_aside)

            AND

                (:posted_after IS NULL
                    OR c.posted_date >= :posted_after)

            AND

                (:close_before IS NULL
                    OR c.close_date <= :close_before)

        )

        SELECT *

        FROM ranked

        WHERE keyword_score > 0

        ORDER BY keyword_score DESC

        LIMIT :limit

        """
        )

        params = {

            "query": query.strip(),

            "limit": limit,

            "agency": filters.get("agency"),

            # use a different parameter name because :naics
            # is already used for keyword matching
            "naics_filter": filters.get("naics"),

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

                "keyword_score":
                    float(row.keyword_score),

                "keyword_match_type":
                    row.keyword_match_type

            })

        return results


keyword_retriever = KeywordRetriever()