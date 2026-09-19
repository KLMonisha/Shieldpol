from app.data_wash import restore, sanitize


def test_indian_pii_is_redacted():
    text = (
        "Priya's PAN is ABCDE1234F and "
        "her phone is +91 9876543210."
    )

    result = sanitize(text)

    assert "ABCDE1234F" not in result.sanitized_text
    assert "+91 9876543210" not in result.sanitized_text

    assert "[PAN_1]" in result.sanitized_text
    assert "[PHONE_1]" in result.sanitized_text


def test_original_values_can_be_restored():
    text = (
        "Priya's PAN is ABCDE1234F and "
        "her phone is +91 9876543210."
    )

    result = sanitize(text)

    model_response = (
        "The customer [PERSON_1] can be contacted "
        "using [PHONE_1]."
    )

    restored = restore(
        model_response,
        result.vault,
    )

    assert "[PHONE_1]" not in restored
    assert "+91 9876543210" in restored


def test_clean_text_is_unchanged():
    text = "Please summarize this customer complaint."

    result = sanitize(text)

    assert result.sanitized_text == text
    assert result.detections == []
    assert len(result.vault) == 0

def test_raw_pii_never_appears_in_sanitized_text():
    text = (
        "Student details: "
        "Aadhaar 1234 5678 9012, "
        "PAN ABCDE1234F, "
        "phone +91 9876543210."
    )

    result = sanitize(text)

    for detection in result.detections:
        assert detection.value not in result.sanitized_text

def test_vault_is_request_scoped():
    first = sanitize(
        "PAN ABCDE1234F"
    )

    second = sanitize(
        "PAN XYZAB5678C"
    )

    assert first.vault.restore(
        "[PAN_1]"
    ) == "ABCDE1234F"

    assert second.vault.restore(
        "[PAN_1]"
    ) == "XYZAB5678C"