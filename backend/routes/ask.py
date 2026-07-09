from flask import Blueprint, request, jsonify

from services.search_service import search_service
from services.llm_answer_generator import answer_generator


ask_bp = Blueprint(
    "ask",
    __name__,
    url_prefix="/ask"
)


@ask_bp.get("")
def ask():

    query = request.args.get("q")

    if not query:
        return jsonify({
            "error": "Missing query"
        }), 400


    #
    # Retrieve
    #

    results = search_service.search(
        query=query
    )


    #
    # Generate answer
    #

    answer = answer_generator.generate(
        query=query,
        results=results
    )


    return jsonify({

        "query": query,

        "answer": answer,

        "results": results

    })