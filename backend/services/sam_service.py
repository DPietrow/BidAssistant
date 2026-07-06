import json
import logging
from pathlib import Path
from datetime import datetime, date
from typing import List, Optional

import requests

from config import Config

logger = logging.getLogger(__name__)


class SAMService:
    """
    Handles communication with SAM.gov.

    During development:
        Reads opportunities from sample_contracts.json.

    Production:
        Queries the SAM.gov Opportunities API.

    This service never writes to the database.
    It only returns normalized dictionaries.
    """

    def __init__(self):

        self.mode = getattr(Config, "SAM_MODE", "mock").lower()

        self.mock_file = (
            Path(__file__).parent.parent
            / "data"
            / "sample_contracts.json"
        )

    ####################################################################
    # Public API
    ####################################################################

    def health(self):

        return {
            "status": "healthy",
            "mode": self.mode
        }

    def search(
        self,
        keywords: Optional[List[str]] = None,
        naics: Optional[List[str]] = None,
        posted_after: Optional[date] = None,
        posted_before: Optional[date] = None,
        limit: int = 100
    ) -> List[dict]:

        logger.info("SAM search starting...")

        if self.mode == "mock":
            contracts = self._search_mock()
        else:
            contracts = self._search_live()

        logger.info(f"Loaded {len(contracts)} contracts")

        if keywords:
            contracts = self._filter_keywords(
                contracts,
                keywords
            )

        if naics:
            contracts = self._filter_naics(
                contracts,
                naics
            )

        if posted_after or posted_before:
            contracts = self._filter_dates(
                contracts,
                posted_after,
                posted_before
            )

        contracts = [
            self._normalize(c)
            for c in contracts
        ]

        logger.info(f"Returning {len(contracts[:limit])} contracts")

        return contracts[:limit]

    ####################################################################
    # Mock implementation
    ####################################################################

    def _search_mock(self):

        logger.info(
            f"Loading mock contracts from {self.mock_file}"
        )

        with open(self.mock_file, encoding="utf-8") as f:
            return json.load(f)

    ####################################################################
    # Live implementation (placeholder)
    ####################################################################

    def _search_live(self):

        logger.info("Calling SAM.gov API")

        api_key = Config.SAM_API_KEY

        url = Config.SAM_API_URL

        headers = {
            "X-Api-Key": api_key
        }

        params = {
            # Populate later
        }

        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        #
        # We'll normalize the SAM.gov schema later.
        #
        return data.get("opportunities", [])

    ####################################################################
    # Filters
    ####################################################################

    def _filter_keywords(
        self,
        contracts,
        keywords
    ):

        keywords = [
            k.lower()
            for k in keywords
        ]

        results = []

        for contract in contracts:

            text = " ".join([
                str(contract.get("title", "")),
                str(contract.get("description", "")),
                " ".join(contract.get("keywords", []))
            ]).lower()

            if any(
                keyword in text
                for keyword in keywords
            ):
                results.append(contract)

        logger.info(
            f"Keyword filter returned {len(results)}"
        )

        return results

    def _filter_naics(
        self,
        contracts,
        naics
    ):

        naics = set(naics)

        results = [

            c

            for c in contracts

            if c.get("naics") in naics

        ]

        logger.info(
            f"NAICS filter returned {len(results)}"
        )

        return results

    def _filter_dates(
        self,
        contracts,
        after,
        before
    ):

        results = []

        for contract in contracts:

            posted = datetime.strptime(
                contract["posted_date"],
                "%Y-%m-%d"
            ).date()

            if after and posted < after:
                continue

            if before and posted > before:
                continue

            results.append(contract)

        logger.info(
            f"Date filter returned {len(results)}"
        )

        return results

    ####################################################################
    # Normalization
    ####################################################################

    def _normalize(self, contract):

        """
        Returns Athena's canonical schema.
        """

        return {

            "sam_id": contract.get("sam_id"),

            "title": contract.get("title"),

            "description": contract.get("description"),

            "agency": contract.get("agency"),

            "office": contract.get("office"),

            "naics": contract.get("naics"),

            "psc": contract.get("psc"),

            "place_of_performance":
                contract.get("place_of_performance"),

            "posted_date":
                contract.get("posted_date"),

            "close_date":
                contract.get("close_date"),

            "notice_type":
                contract.get("notice_type"),

            "set_aside":
                contract.get("set_aside"),

            "estimated_value":
                contract.get("estimated_value"),

            "keywords":
                contract.get("keywords", []),

            "url":
                contract.get("url")

        }


sam_service = SAMService()