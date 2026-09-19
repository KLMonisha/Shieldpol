from app.detectors import detect_pii


def test_indian_pii_detection():
    text = (
        "Customer Priya has PAN ABCDE1234F, "
        "Aadhaar 1234 5678 9012, "
        "phone +91 9876543210, "
        "GSTIN 29ABCDE1234F1Z5, "
        "and IFSC HDFC0001234."
    )

    detections = detect_pii(text)

    detected_types = {
        detection.entity_type
        for detection in detections
    }

    assert "PAN" in detected_types
    assert "AADHAAR" in detected_types
    assert "PHONE" in detected_types
    assert "GSTIN" in detected_types
    assert "IFSC" in detected_types