import hashlib
import base58

# The 7 parts identified in the puzzle solution records
parts = [
    "causality", 
    "Safenet", 
    "Luna", 
    "HSM", 
    "11110", 
    "is", 
    "lastwordsbeforearchichoicethispassword"
]

# The "Last Command": Hash the concatenated string
final_seed = "".join(parts)
final_hex = hashlib.sha256(final_seed.encode()).hexdigest()

def to_wif(hex_key):
    extended = b'\x80' + bytes.fromhex(hex_key) + b'\x01'
    h = hashlib.sha256(hashlib.sha256(extended).digest()).digest()
    return base58.b58encode(extended + h[:4]).decode()

print(f"Concatenated Seed: {final_seed}")
print(f"Final Prize Hex: {final_hex}")
print(f"Final Prize WIF: {to_wif(final_hex)}")