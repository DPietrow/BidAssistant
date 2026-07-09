from flask import Blueprint, request, jsonify

from services.search_service import search_service
from services.llm_answer_generator import answer_generator


ask_bp = Blueprint(
    "ask",
    __name__,
    url_prefix="/ask"
)


@ask_bp.post("")
def ask():

    data = request.json


    query = data.get(
        "query"
    )


    filters = data.get(
        "filters",
        {}
    )


    if not query:

        return jsonify(
            {
                "error":
                "Missing query"
            }
        ),400


    response = search_service.search(

        query=query,

        filters=filters

    )


    return jsonify(
        {
            "query": query,

            "answer": response["answer"],

            "results": response["results"]
        }
    )