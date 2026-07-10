from flask import Blueprint, request, jsonify

from services.athena_service import athena_service
from services.athena_memory import memory


athena_bp = Blueprint(
    "athena",
    __name__,
    url_prefix="/athena"
)



@athena_bp.post("/chat")
def chat():


    data = request.json


    session_id = data.get(
        "session_id"
    )


    if not session_id:

        session_id = memory.create_session()



    message = data.get(
        "message"
    )


    context = data.get(
        "context",
        {}
    )


    search_results = context.get(
        "searchResults",
        []
    )


    selected_contracts = context.get(
        "selectedContracts",
        []
    )



    response = athena_service.chat(

        session_id=session_id,

        message=message,

        search_results=search_results,

        selected_contracts=selected_contracts

    )


    return jsonify({

        "session_id":
            session_id,

        **response

    })