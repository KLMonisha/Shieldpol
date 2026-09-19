from app.llm import MockLLMClient
from app.shieldpol import process_request


def test_shieldpol_does_not_send_raw_pii_to_llm():
    prompt = (
        "Analyze this customer. "
        "PAN ABCDE1234F. "
        "Phone +91 9876543210."
    )

    result = process_request(
        prompt,
        MockLLMClient(),
    )

    assert "ABCDE1234F" not in result["sanitized_prompt"]
    assert "+91 9876543210" not in result["sanitized_prompt"]

    assert "[PAN_1]" in result["sanitized_prompt"]
    assert "[PHONE_1]" in result["sanitized_prompt"]


def test_shieldpol_restores_pii_for_user():
    prompt = (
        "Customer PAN ABCDE1234F. "
        "Phone +91 9876543210."
    )

    result = process_request(
        prompt,
        MockLLMClient(),
    )

    assert "ABCDE1234F" in result["restored_response"]
    assert "+91 9876543210" in result["restored_response"]


def test_clean_request_passes_unchanged():
    prompt = "Summarize this customer complaint."

    result = process_request(
        prompt,
        MockLLMClient(),
    )

    assert result["sanitized_prompt"] == prompt
    assert result["detections"] == []
    assert result["restored_response"] == result["response"]