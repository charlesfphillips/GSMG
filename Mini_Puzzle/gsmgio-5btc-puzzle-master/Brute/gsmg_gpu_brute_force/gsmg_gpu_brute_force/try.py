import hashlib

# Concatenation of all known parts
parts = ["causality", "Safenet", "Luna", "HSM", "11110", "is", "lastwordsbeforearchichoice", "thispassword"]
final_string = "".join(parts)

# Try SHA256 of the combined string
k_final_hex = hashlib.sha256(final_string.encode()).hexdigest()
print(f"Concatenated Key: {k_final_hex}")