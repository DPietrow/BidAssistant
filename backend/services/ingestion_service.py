from datetime import datetime

from database import db
from models import Contract


class IngestionService:

    def normalize(self, raw: dict) -> dict:

        return {

            "sam_id": raw.get("sam_id"),

            "title": (raw.get("title") or "").strip(),

            "description": (raw.get("description") or "").strip(),

            "agency": (raw.get("agency") or "").strip(),

            "naics": raw.get("naics"),

            "posted_date": self._parse_date(raw.get("posted_date")),

            "close_date": self._parse_date(raw.get("close_date")),

            "response_deadline": self._parse_datetime(
                raw.get("response_deadline")
            ),

            "url": raw.get("url"),

            "notice_type": raw.get("notice_type"),

            "set_aside": raw.get("set_aside"),

            "status": raw.get("status", "ACTIVE"),

            #
            # searchable blob
            #
            "raw_text": self._build_raw_text(raw),

            #
            # later
            #
            "semantic_score": None,

            "bid_score": None,

            "embedding_created": False
        }

    ##################################################################

    def upsert_many(self, contracts: list[dict]):

        inserted = 0
        updated = 0

        for raw in contracts:

            normalized = self.normalize(raw)

            existing = Contract.query.filter_by(
                sam_id=normalized["sam_id"]
            ).first()

            if existing:

                self._update(existing, normalized)
                updated += 1

            else:

                contract = Contract(**normalized)

                db.session.add(contract)

                inserted += 1

        db.session.commit()

        return {

            "inserted": inserted,

            "updated": updated,

            "total_processed": inserted + updated

        }

    ##################################################################

    def _update(self, contract: Contract, values: dict):

        for key, value in values.items():

            setattr(contract, key, value)

        contract.updated_at = datetime.utcnow()

    ##################################################################

    def _build_raw_text(self, raw):

        pieces = [

            raw.get("title", ""),

            raw.get("description", ""),

            raw.get("agency", ""),

            raw.get("naics", ""),

            raw.get("notice_type", ""),

            raw.get("set_aside", "")

        ]

        return "\n".join(
            str(x)
            for x in pieces
            if x
        )

    ##################################################################

    def _parse_date(self, value):

        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d"
            ).date()

        except Exception:

            return None

    ##################################################################

    def _parse_datetime(self, value):

        if not value:
            return None

        try:

            return datetime.fromisoformat(
                value.replace("Z", "")
            )

        except Exception:

            return None


ingestion_service = IngestionService()