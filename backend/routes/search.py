from flask import Blueprint, request, jsonify, Response, stream_with_context
import json
import time

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


    filters = data.get("filters") or {}


    filters = {
        key:value
        for key,value in filters.items()
        if value not in ("", None)
    }

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

@search_bp.post("/stream")
def athena_search_stream():

    data = request.json


    query = data.get(
        "query",
        ""
    )


    filters = data.get("filters") or {}


    # normalize filters exactly like normal search
    filters = {
        key:value
        for key,value in filters.items()
        if value not in ("", None)
    }



    if not query:

        return jsonify(
            {
                "error":"Missing query"
            }
        ),400



    def generate():


        yield (
            "event: status\n"
            f"data: {json.dumps({'stage':'discovering'})}\n\n"
        )


        time.sleep(.5)



        yield (
            "event: status\n"
            f"data: {json.dumps({'stage':'analyzing'})}\n\n"
        )



        print("STREAM QUERY:", query)
        print("STREAM FILTERS:", filters)



        response = search_service.search(
            query=query,
            filters=filters
        )



        print(
            "STREAM RESULT COUNT:",
            len(response.get("results", []))
        )



        yield (
            "event: status\n"
            f"data: {json.dumps({'stage':'matching'})}\n\n"
        )


        time.sleep(.5)



        yield (
            "event: status\n"
            f"data: {json.dumps({'stage':'ranking'})}\n\n"
        )


        time.sleep(.5)



        yield (
            "event: complete\n"
            f"data: {json.dumps(response)}\n\n"
        )



    return Response(

        stream_with_context(generate()),

        mimetype="text/event-stream",

        headers={
            "Cache-Control":"no-cache",
            "X-Accel-Buffering":"no"
        }

    )