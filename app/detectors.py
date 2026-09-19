import re
from dataclasses import dataclass


@dataclass
class Detection:
    entity_type: str
    value: str
    start: int
    end: int


PATTERNS = {
    "PAN": re.compile(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    ),

    "AADHAAR": re.compile(
        r"\b\d{4}\s\d{4}\s\d{4}\b"
    ),

    "GSTIN": re.compile(
        r"\b\d{2}[A-Z]{5}\d{4}[A-Z][A-Z0-9]Z[A-Z0-9]\b"
    ),

    "IFSC": re.compile(
        r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
    ),

    "PHONE": re.compile(
        r"(?<!\d)(?:\+91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?!\d)"
    ),

    "EMAIL": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "UPI": re.compile(
        r"\b[a-zA-Z0-9._-]+@[a-zA-Z][a-zA-Z0-9.-]*\b"
    ),

    "BANK_ACCOUNT": re.compile(
        r"(?i)(?<=bank account:\s)\d{9,18}\b"
    ),
}


# Higher priority patterns should win when
# multiple detectors match the same text.
PRIORITY = {
    "PAN": 100,
    "GSTIN": 100,
    "AADHAAR": 100,
    "IFSC": 100,
    "BANK_ACCOUNT": 100,
    "PHONE": 90,
    "EMAIL": 80,
    "UPI": 70,
}


def _overlaps(first: Detection, second: Detection) -> bool:
    return (
        first.start < second.end
        and second.start < first.end
    )


def detect_pii(text: str) -> list[Detection]:
    candidates = []

    for entity_type, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            candidates.append(
                Detection(
                    entity_type=entity_type,
                    value=match.group(),
                    start=match.start(),
                    end=match.end(),
                )
            )

    # Highest-priority detections first.
    candidates.sort(
        key=lambda item: (
            -PRIORITY[item.entity_type],
            item.start,
        )
    )

    selected = []

    for candidate in candidates:
        if any(_overlaps(candidate, existing) for existing in selected):
            continue

        selected.append(candidate)

    selected.sort(key=lambda item: item.start)

    return selected