from datetime import datetime

from flask import Blueprint, jsonify, request

from models import Contract

contracts_bp = Blueprint(
    "contracts",
    __name__,
    url_prefix="/contracts"
)


#######################################################################
# GET /contracts
#######################################################################

@contracts_bp.get("")
def get_contracts():

    query = Contract.query

    ###################################################################
    # Keyword search
    ###################################################################

    keywords = request.args.get("keyword")

    if keywords:

        keyword_list = [
            k.strip()
            for k in keywords.split(",")
            if k.strip()
        ]

        for keyword in keyword_list:

            query = query.filter(
                Contract.raw_text.ilike(f"%{keyword}%")
            )

    ###################################################################
    # NAICS
    ###################################################################

    naics = request.args.get("naics")

    if naics:

        naics_list = [
            n.strip()
            for n in naics.split(",")
            if n.strip()
        ]

        query = query.filter(
            Contract.naics.in_(naics_list)
        )

    ###################################################################
    # Posted Date
    ###################################################################

    posted_after = request.args.get("posted_after")

    if posted_after:

        query = query.filter(
            Contract.posted_date >= datetime.strptime(
                posted_after,
                "%Y-%m-%d"
            ).date()
        )

    posted_before = request.args.get("posted_before")

    if posted_before:

        query = query.filter(
            Contract.posted_date <= datetime.strptime(
                posted_before,
                "%Y-%m-%d"
            ).date()
        )

    ###################################################################
    # Status
    ###################################################################

    status = request.args.get("status")

    if status:

        query = query.filter(
            Contract.status == status
        )

    ###################################################################
    # Set Aside
    ###################################################################

    set_aside = request.args.get("set_aside")

    if set_aside:

        query = query.filter(
            Contract.set_aside == set_aside
        )

    ###################################################################
    # Notice Type
    ###################################################################

    notice_type = request.args.get("notice_type")

    if notice_type:

        query = query.filter(
            Contract.notice_type == notice_type
        )

    ###################################################################
    # Sorting
    ###################################################################

    sort = request.args.get(
        "sort",
        default="posted_date"
    )

    direction = request.args.get(
        "direction",
        default="desc"
    )

    sort_column = getattr(
        Contract,
        sort,
        Contract.posted_date
    )

    if direction.lower() == "asc":

        query = query.order_by(sort_column.asc())

    else:

        query = query.order_by(sort_column.desc())

    ###################################################################
    # Limit
    ###################################################################

    limit = request.args.get(
        "limit",
        default=100,
        type=int
    )

    contracts = query.limit(limit).all()

    ###################################################################
    # Response
    ###################################################################

    summary = []

    for c in contracts:

        summary.append({

            "sam_id": c.sam_id,

            "title": c.title,

            "agency": c.agency,

            "naics": c.naics,

            "posted_date": c.posted_date,

            "close_date": c.close_date,

            "status": c.status,

            "notice_type": c.notice_type,

            "set_aside": c.set_aside,

            "semantic_score": c.semantic_score

        })

    return jsonify(summary)


#######################################################################
# GET /contracts/<sam_id>
#######################################################################

@contracts_bp.get("/<sam_id>")
def get_contract(sam_id):

    contract = Contract.query.filter_by(
        sam_id=sam_id
    ).first()

    if not contract:

        return (
            jsonify({
                "error": "Contract not found"
            }),
            404
        )

    return jsonify({

        "sam_id": contract.sam_id,

        "title": contract.title,

        "description": contract.description,

        "agency": contract.agency,

        "naics": contract.naics,

        "posted_date": contract.posted_date,

        "close_date": contract.close_date,

        "url": contract.url,

        "status": contract.status,

        "notice_type": contract.notice_type,

        "set_aside": contract.set_aside,

        "raw_text": contract.raw_text,

        "semantic_score": contract.semantic_score,

        "embedding_created": contract.embedding_created

    })


#######################################################################
# GET /contracts/health
#######################################################################

@contracts_bp.get("/health")
def health():

    return jsonify({

        "status": "healthy",

        "database": "connected"

    })