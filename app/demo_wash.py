from app.data_wash import sanitize, restore


prompt = (
    "Please analyze this student record. "
    "Student name is Priya Nair. "
    "Aadhaar is 1234 5678 9012. "
    "PAN is ABCDE1234F. "
    "Phone is +91 9876543210."
)

print("=" * 60)
print("SHIELDPOL DATA WASH")
print("=" * 60)

print("\nORIGINAL PROMPT:")
print(prompt)

result = sanitize(prompt)

print("\nDETECTED DATA:")
for detection in result.detections:
    print(
        f"{detection.entity_type}: "
        f"{detection.value}"
    )

print("\nSANITIZED PROMPT:")
print(result.sanitized_text)

print("\nSECURE MAPPING:")
for token, value in result.mapping.items():
    print(f"{token} -> {value}")

model_response = (
    "The student [PERSON_1] can be contacted at "
    "[PHONE_1]."
)

print("\nLLM RESPONSE:")
print(model_response)

restored_response = restore(
    model_response,
    result.mapping,
)

print("\nRESTORED RESPONSE:")
print(restored_response)