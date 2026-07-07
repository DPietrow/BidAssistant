from flask import Blueprint, jsonify

from services.embedding_pipeline import embedding_pipeline


embedding_bp = Blueprint(
    "embeddings",
    __name__,
    url_prefix="/embeddings"
)


@embedding_bp.post("/process")
def process_embeddings():

    result = (
        embedding_pipeline
        .process_pending(
            batch_size=10
        )
    )


    return jsonify(result)