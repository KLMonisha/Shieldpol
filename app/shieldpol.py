from app.data_wash import sanitize, restore
from app.llm import LLMClient


def process_request(
    prompt: str,
    llm_client: LLMClient,
) -> dict:
    """Process an LLM request through the ShieldPol privacy boundary."""

    wash_result = sanitize(prompt)

    sanitized_response = llm_client.generate(
        wash_result.sanitized_text
    )

    restored_response = restore(
        sanitized_response,
        wash_result.vault,
    )

    return {
        "original_prompt": prompt,
        "sanitized_prompt": wash_result.sanitized_text,
        "response": sanitized_response,
        "restored_response": restored_response,
        "detections": wash_result.detections,
        "vault": wash_result.vault,
    }