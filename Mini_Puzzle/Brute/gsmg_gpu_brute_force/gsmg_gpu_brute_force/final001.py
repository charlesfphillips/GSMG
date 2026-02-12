import hashlib
import base58

# The full 7-part sequence
parts = [
    "causalitySafenetLunaHSM1105islastwordsbeforearchichoicethispassword"
]

# Join them exactly as written
final_seed = "".join(parts)

# The "Last Command": Single SHA-256
final_hex = hashlib.sha256(final_seed.encode()).hexdigest()

def to_wif(hex_key):
    # Standard compressed WIF format
    extended = b'\x80' + bytes.fromhex(hex_key) + b'\x01'
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    return base58.b58encode(extended + checksum).decode()

print(f"Full Seed: {final_seed}")
print(f"Final WIF: {to_wif(final_hex)}")