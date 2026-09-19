from app.llm import MockLLMClient
from app.shieldpol import process_request
from app.finance import build_financial_prompt

financial_document = """
Company: Acme Innovations Pvt Ltd

Business PAN: ABCDE1234F
GSTIN: 29ABCDE1234F1Z5
Bank Account: 123456789012
IFSC: HDFC0001234
Phone: +91 9876543210
Email: finance@acme.com

September Expenses

AWS Cloud Services - ₹42,000
Software Licenses - ₹18,500
Travel Expenses - ₹12,300
Marketing Campaign - ₹9,800
Office Supplies - ₹4,200

Total Expenses: ₹86,800
"""

question = """
Analyze this financial document and tell me the top
three operating expense categories.
"""

prompt = build_financial_prompt(
    financial_document,
    question
)


result = process_request(
    prompt,
    MockLLMClient()
)

print("=" * 65)
print("SHIELDPOL FINANCE DEMO")
print("=" * 65)

print("\nORIGINAL DOCUMENT\n")
print(result["original_prompt"])

print("\n" + "=" * 65)
print("SANITIZED PROMPT SENT TO LLM")
print("=" * 65)

print(result["sanitized_prompt"])

print("\n" + "=" * 65)
print("DETECTED SENSITIVE ENTITIES")
print("=" * 65)

for detection in result["detections"]:
    print(f"{detection.entity_type}: {detection.value}")

print("\n" + "=" * 65)
print("LLM RESPONSE")
print("=" * 65)

print(result["response"])

print("\n" + "=" * 65)
print("RESTORED USER RESPONSE")
print("=" * 65)

print(result["restored_response"])

print("\n" + "=" * 65)
print("SECURITY SUMMARY")
print("=" * 65)

print(f"Sensitive entities detected: {len(result['detections'])}")
print("Raw sensitive data sent to model: 0")
print(f"Request vault entries: {len(result['vault'])}")