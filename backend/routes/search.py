from flask import Blueprint, request, jsonify

from services.search_service import search_service


search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)


@search_bp.get("")
def search():


    query = request.args.get("q")


    if not query:

        return jsonify(
            {
                "error":
                "Missing query"
            }
        ), 400


    results = search_service.search(
        query
    )


    return jsonify(
        {
            "query": query,
            "results": results
        }
    )