import hashlib

def base58_encode(raw_bytes):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(raw_bytes, 'big')
    res = ""
    while n > 0:
        n, r = divmod(n, 58)
        res = alphabet[r] + res
    return res

# The final combined hex key you calculated
hex_key = "f8811be90a9d71efe34b3c196e1c92e44aa9e67a7e2f6aa52e39dfe3de4173fb"
key_bytes = bytes.fromhex(hex_key)

# 1. Add 0x80 prefix (Bitcoin Mainnet)
# 2. Add 0x01 suffix (Compressed key flag)
extended = b'\x80' + key_bytes + b'\x01'

# 3. Double SHA-256 for the 4-byte checksum
h1 = hashlib.sha256(extended).digest()
h2 = hashlib.sha256(h1).digest()
final_data = extended + h2[:4]

# 4. Final WIF String
wif = base58_encode(final_data)
print(f"Your WIF Key: {wif}")