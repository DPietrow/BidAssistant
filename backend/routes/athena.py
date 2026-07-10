from flask import Blueprint, Response, request, jsonify
import json


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

@athena_bp.post("/chat/stream")
def chat_stream():


    data=request.json


    session_id = data.get(
        "session_id"
    )


    if not session_id:

        session_id = memory.create_session()



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



    def generate():


        for chunk in athena_service.stream_chat(

            session_id=session_id,

            message=message,

            search_results=search_results,

            selected_contracts=selected_contracts

        ):


            yield (

                f"data:{json.dumps(chunk)}\n\n"

            )



    return Response(

        generate(),

        mimetype="text/event-stream"

    )