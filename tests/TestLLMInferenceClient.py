from app.qualifications.llm_inference_client import LLMInferenceResponse


def test_openrouter_usage_fields_are_extracted():
    response = LLMInferenceResponse(
        endpoint="https://openrouter.ai/api/v1/chat/completions",
        request_json={"hello": "world"},
        response_json={
            "usage": {
                "prompt_tokens": 123,
                "completion_tokens": 45,
                "cost": "0.00067",
            }
        },
    )

    assert response.cost == 0.00067
    assert response.input_tokens == 123
    assert response.output_tokens == 45


if __name__ == "__main__":
    test_openrouter_usage_fields_are_extracted()
    print("LLM inference client usage extraction ok")
