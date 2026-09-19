from abc import ABC, abstractmethod
import re
import boto3

class LLMClient(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class MockLLMClient(LLMClient):
    def generate(self, prompt: str) -> str:
        expenses = re.findall(
            r"(.+?)\s*-\s*₹([\d,]+)",
            prompt
        )

        parsed = []

        for category, amount in expenses:
            value = int(amount.replace(",", ""))
            parsed.append((category.strip(), value))

        if parsed:
            parsed.sort(key=lambda item: item[1], reverse=True)

            top_three = parsed[:3]

            lines = ["Top three operating expenses:"]

            for index, (category, amount) in enumerate(
                top_three,
                start=1
            ):
                lines.append(
                    f"{index}. {category}: ₹{amount:,}"
                )

            return "\n".join(lines)

        # Generic fallback used by security/unit tests.
        tokens = re.findall(
            r"\[(?:PAN|AADHAAR|GSTIN|BANK_ACCOUNT|IFSC|PHONE|EMAIL|UPI)_\d+\]",
            prompt
        )

        if tokens:
            return "Processed sensitive information: " + ", ".join(tokens)

        return "The request has been processed."

class BedrockLLMClient(LLMClient):
    def __init__(
        self,
        model_id: str = "global.anthropic.claude-haiku-4-5-20251001-v1:0",
        region_name: str = "ap-south-2",
    ):
        self.model_id = model_id
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
        )

    def generate(self, prompt: str) -> str:
        response = self.client.converse(
            modelId=self.model_id,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ],
                }
            ],
            inferenceConfig={
                "maxTokens": 512,
                "temperature": 0.2,
            },
        )

        return response["output"]["message"]["content"][0]["text"]