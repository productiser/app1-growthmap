import requests
import json
from dataclasses import dataclass
from typing import Any
import os
from pathlib import Path

OPENROUTER_BASE_URL="https://openrouter.ai/api/v1/chat/completions"
SYSTEM_PROMPT_PATH = Path(__file__).with_name("prompt.txt")

class LLMInferenceConfigError(RuntimeError):
    pass

@dataclass
class LLMInferenceResponse:
    endpoint: str
    request_json: dict[str, Any]
    response_json: dict[str, Any]

    @property
    def cost(self) -> float | None:
        usage = self.response_json.get("usage") or {}
        cost = usage.get("cost")
        return float(cost) if cost is not None else None

    @property
    def input_tokens(self) -> int | None:
        usage = self.response_json.get("usage") or {}
        prompt_tokens = usage.get("prompt_tokens")
        return int(prompt_tokens) if prompt_tokens is not None else None

    @property
    def output_tokens(self) -> int | None:
        usage = self.response_json.get("usage") or {}
        completion_tokens = usage.get("completion_tokens")
        return int(completion_tokens) if completion_tokens is not None else None
    

class LLMInferenceClient: 
    def __init__(self, apiKey: str | None = None):
        self.apiKey = (apiKey or os.getenv("OPENROUTER_API_KEY") or "").strip()
        if not self.apiKey :
            raise LLMInferenceConfigError(
                "OPENROUTER APIKEY CONFIG NOT SETUP"
            )

    @staticmethod
    def get_response_format() -> dict[str, Any]:
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "qualification_inference",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "keyword_classifications": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "keyword": {"type": "string"},
                                    "classification": {
                                        "type": "string",
                                        "enum": [
                                            "business_brand",
                                            "other_company_brand",
                                            "relevant_commercial",
                                            "relevant_informational",
                                            "irrelevant_or_ambiguous",
                                        ],
                                    },
                                    "reason": {"type": "string"},
                                },
                                "required": [
                                    "keyword",
                                    "classification",
                                    "reason",
                                ],
                                "additionalProperties": False,
                            },
                        },
                        "recommendation": {
                            "type": "object",
                            "properties": {
                                "recommended_outcome": {
                                    "type": "string",
                                    "enum": [
                                        "weak_prospect",
                                        "possible_prospect",
                                    ],
                                },
                                "confidence_score": {
                                    "type": "number",
                                    "minimum": 0.0,
                                    "maximum": 1.0,
                                },
                                "reason": {"type": "string"},
                            },
                            "required": [
                                "recommended_outcome",
                                "confidence_score",
                                "reason",
                            ],
                            "additionalProperties": False,
                        },
                        "evidence_summary": {"type": "string"},
                        "verified_signals": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "limitations": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "headline": {"type": "string"},
                        "explanation": {"type": "string"},
                    },
                    "required": [
                        "keyword_classifications",
                        "recommendation",
                        "evidence_summary",
                        "verified_signals",
                        "limitations",
                        "headline",
                        "explanation",
                    ],
                    "additionalProperties": False,
                }
            },
        }

    def get_llm_inference_payload(self,payload: dict[str, Any]):
        return {
            "model": "~openai/gpt-latest",
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT_PATH.read_text(encoding="utf-8"),
                },
                {
                    "role": "user",
                    "content": json.dumps(payload),
                },
            ],
            "response_format":self.get_response_format()      
        }

    def _post(self, endpoint: str, payload: dict[str, Any]) -> LLMInferenceResponse:
        llm_payload = self.get_llm_inference_payload(payload)
        response = requests.post(
            url=endpoint,
            headers={
                "Authorization": f"Bearer {self.apiKey}",
                "HTTP-Referer": "https://wwww.dorianaudits.uk",
                "X-OpenRouter-Title": "https://wwww.dorianaudits.uk",
                "Content-Type": "application/json",
            },
            data=json.dumps(llm_payload).encode("utf-8"),

        )
        response.raise_for_status()
        return LLMInferenceResponse(
            endpoint=endpoint,
            request_json=payload,
            response_json=response.json(),
        )
    # Public method for this class
    def run_qualification_inference(
        self,
        payload: dict[str, Any],
    ) -> LLMInferenceResponse:
        return self._post(
            endpoint=OPENROUTER_BASE_URL,
            payload=payload,
        )
