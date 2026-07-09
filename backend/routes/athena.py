from flask import Blueprint, request, jsonify

from services.athena_service import athena_service


athena_bp = Blueprint(
    "athena",
    __name__,
    url_prefix="/athena"
)


@athena_bp.post("/chat")
def chat():

    data=request.json


    message=data.get(
        "message"
    )


    context=data.get(
        "context",
        {}
    )


    search_results=context.get(
        "searchResults",
        []
    )

    selected_contracts=context.get(
        "selectedContracts",
        []
    )


    response = athena_service.chat(

        message=message,

        search_results=search_results,

        selected_contracts=selected_contracts

    )


    return jsonify(response)