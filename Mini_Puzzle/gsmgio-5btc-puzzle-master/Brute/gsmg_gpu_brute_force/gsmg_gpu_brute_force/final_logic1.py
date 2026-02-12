import hashlib
import base58

# The "Command" + "Better 1/2" + "1/2"
# Mimicking a terminal command: command arg1 arg2
final_seed = "causality lastwordsbeforearchichoice thispassword"

# Final SHA-256
final_hex = hashlib.sha256(final_seed.encode()).hexdigest()

def to_wif(hex_key):
    # Compressed WIF format
    extended = b'\x80' + bytes.fromhex(hex_key) + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

print(f"Final Seed: {final_seed}")
print(f"Final WIF: {to_wif(final_hex)}")