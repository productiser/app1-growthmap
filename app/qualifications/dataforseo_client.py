import base64
import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


DATAFORSEO_BASE_URL = "https://api.dataforseo.com/v3"
RANKED_KEYWORDS_ENDPOINT = "/dataforseo_labs/google/ranked_keywords/live"
ON_PAGE_INSTANT_PAGES_ENDPOINT = "/on_page/instant_pages"


class DataForSeoConfigurationError(RuntimeError):
    pass


class DataForSeoApiError(RuntimeError):
    pass


@dataclass
class DataForSeoResponse:
    endpoint: str
    request_json: list[dict[str, Any]]
    response_json: dict[str, Any]

    @property
    def cost(self) -> float | None:
        cost = self.response_json.get("cost")
        return float(cost) if cost is not None else None

    @property
    def provider_task_id(self) -> str | None:
        tasks = self.response_json.get("tasks") or []
        if not tasks:
            return None
        return tasks[0].get("id")


class DataForSeoClient:
    def __init__(self, login: str | None = None, password: str | None = None):
        self.login = (login or os.getenv("DATAFORSEO_LOGIN") or "").strip()
        self.password = (password or os.getenv("DATAFORSEO_PASSWORD") or "").strip()

        if not self.login or not self.password:
            raise DataForSeoConfigurationError(
                "DATAFORSEO_LOGIN and DATAFORSEO_PASSWORD are required"
            )

    def fetch_ranked_keywords(
        self,
        target_domain: str,
        location_code: int,
        language_code: str,
        limit: int = 20,
    ) -> DataForSeoResponse:
        payload = build_ranked_keywords_payload(
            target_domain=target_domain,
            location_code=location_code,
            language_code=language_code,
            limit=limit,
        )
        return self._post(RANKED_KEYWORDS_ENDPOINT, payload)

    def fetch_on_page(self, url: str) -> DataForSeoResponse:
        payload = build_on_page_payload(url)
        return self._post(ON_PAGE_INSTANT_PAGES_ENDPOINT, payload)

    def _post(self, endpoint: str, payload: list[dict[str, Any]]) -> DataForSeoResponse:
        request = Request(
            url=f"{DATAFORSEO_BASE_URL}{endpoint}",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Basic {self._basic_auth_token()}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=30) as response:
                response_json = json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            body = error.read().decode("utf-8")
            raise DataForSeoApiError(
                f"DataForSEO HTTP {error.code} for {endpoint}: {body}"
            ) from error
        except URLError as error:
            raise DataForSeoApiError(
                f"DataForSEO request failed for {endpoint}: {error.reason}"
            ) from error

        if response_json.get("status_code") != 20000:
            raise DataForSeoApiError(
                "DataForSEO returned status "
                f"{response_json.get('status_code')}: {response_json.get('status_message')}"
            )

        return DataForSeoResponse(
            endpoint=endpoint,
            request_json=payload,
            response_json=response_json,
        )

    def _basic_auth_token(self) -> str:
        raw_token = f"{self.login}:{self.password}".encode("utf-8")
        return base64.b64encode(raw_token).decode("ascii")


def build_ranked_keywords_payload(
    target_domain: str,
    location_code: int,
    language_code: str,
    limit: int = 20,
) -> list[dict[str, Any]]:
    return [
        {
            "target": target_domain,
            "location_code": location_code,
            "language_code": language_code,
            "filters": [
                ["keyword_data.keyword_info.search_volume", "<>", 0],
                "and",
                [
                    ["ranked_serp_element.serp_item.type", "<>", "paid"],
                    "or",
                    ["ranked_serp_element.serp_item.is_paid", "=", False],
                ],
            ],
            "limit": limit,
        }
    ]


def build_on_page_payload(url: str) -> list[dict[str, Any]]:
    return [{"url": url}]
