import hashlib
import base58

# The result from your shabe1.py
hex_key = "855411a598c406fe2063cd09136ec19a83ca1de0be77235d45b4bcf80248ff45"
key_bytes = bytes.fromhex(hex_key)

# 1. Add 0x80 prefix and 0x01 suffix (Compressed)
extended = b'\x80' + key_bytes + b'\x01'

# 2. Calculate Checksum (Double SHA-256)
h1 = hashlib.sha256(extended).digest()
h2 = hashlib.sha256(h1).digest()
final_data = extended + h2[:4]

# 3. Base58 Encode
wif = base58.b58encode(final_data).decode('utf-8')
print(f"Final WIF to import: {wif}")