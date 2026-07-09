from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class SearchFilters:

    agency: Optional[str] = None

    naics: Optional[str] = None

    notice_type: Optional[str] = None

    set_aside: Optional[str] = None

    posted_after: Optional[date] = None

    close_before: Optional[date] = None


    @classmethod
    def from_dict(
        cls,
        data
    ):

        if not data:
            return cls()


        return cls(

            agency=data.get(
                "agency"
            ),

            naics=data.get(
                "naics"
            ),

            notice_type=data.get(
                "notice_type"
            ),

            set_aside=data.get(
                "set_aside"
            ),

            posted_after=data.get(
                "posted_after"
            ),

            close_before=data.get(
                "close_before"
            )

        )


    def to_dict(self):

        return {

            "agency": self.agency,

            "naics": self.naics,

            "notice_type": self.notice_type,

            "set_aside": self.set_aside,

            "posted_after": self.posted_after,

            "close_before": self.close_before

        }