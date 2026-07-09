from flask import Blueprint, request, jsonify

from services.search_service import search_service


search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


@search_bp.post("")
def search():

    data = request.json


    query = data.get(
        "query",
        ""
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
        response
    )