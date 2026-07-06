from flask import Blueprint, jsonify

from services.sam_service import sam_service
from services.ingestion_service import ingestion_service

ingestion_bp = Blueprint(
    "ingestion",
    __name__,
    url_prefix="/ingestion"
)


@ingestion_bp.get("/health")
def health():

    return jsonify({
        "status": "healthy"
    })


@ingestion_bp.post("/run")
def run_ingestion():
    contracts = sam_service.search(limit=10000)

    stats = ingestion_service.upsert_many(contracts)

    return jsonify({
        "success": True,
        "message": "Ingestion completed successfully.",
        "statistics": stats
    })