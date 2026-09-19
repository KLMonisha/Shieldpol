from dataclasses import dataclass

from app.detectors import Detection, detect_pii
from app.token_vault import TokenVault


@dataclass
class WashResult:
    sanitized_text: str
    detections: list[Detection]
    vault: TokenVault


def sanitize(text: str) -> WashResult:
    detections = detect_pii(text)

    vault = TokenVault()

    if not detections:
        return WashResult(
            sanitized_text=text,
            detections=[],
            vault=vault,
        )

    counters = {}
    replacements = []

    for detection in detections:
        entity_type = detection.entity_type

        counters[entity_type] = counters.get(entity_type, 0) + 1
        token = f"[{entity_type}_{counters[entity_type]}]"

        replacements.append((detection, token))

    sanitized = text

    for detection, token in reversed(replacements):
        vault.store(token, detection.value)

        sanitized = (
            sanitized[:detection.start]
            + token
            + sanitized[detection.end:]
        )

    return WashResult(
        sanitized_text=sanitized,
        detections=detections,
        vault=vault,
    )


def restore(text: str, vault: TokenVault) -> str:
    return vault.restore(text)