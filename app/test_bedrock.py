from app.llm import BedrockLLMClient


client = BedrockLLMClient()

response = client.generate(
    "Reply with exactly: ShieldPol Bedrock connection successful."
)

print(response)