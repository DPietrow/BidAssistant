from flask import Blueprint, jsonify

from services.retrieval.keyword_retriever import keyword_retriever


test_search_bp = Blueprint(
    "test_search",
    __name__
)


@test_search_bp.get("/test/keyword")
def test_keyword():

    results = keyword_retriever.search(
        "industrial filtration"
    )

    output = []

    for row in results:

        output.append({

            "contract_id": row.contract_id,

            "title": row.title,

            "agency": row.agency,

            "score": float(
                row.keyword_score
            )

        })

    return jsonify(output)

@test_search_bp.get("/test/semantic")
def test_semantic():

    from services.embedding_service import embedding_service
    from services.retrieval.semantic_retriever import semantic_retriever


    vector = embedding_service.embed_query(
        "industrial filtration"
    )


    rows = semantic_retriever.search(
        vector
    )


    output=[]


    for row in rows:

        output.append({

            "title": row.title,

            "semantic_score":
                float(row.semantic_score)

        })


    return jsonify(output)