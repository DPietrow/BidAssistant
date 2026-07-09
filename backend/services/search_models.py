from dataclasses import dataclass


@dataclass
class SearchFilters:

    agency: list[str] | None = None

    naics: list[str] | None = None

    notice_type: list[str] | None = None

    set_aside: list[str] | None = None

    posted_after: str | None = None

    close_before: str | None = None