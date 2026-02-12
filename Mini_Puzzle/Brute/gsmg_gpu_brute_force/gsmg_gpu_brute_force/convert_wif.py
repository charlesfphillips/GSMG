import hashlib

def base58_encode(raw_bytes):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(raw_bytes, 'big')
    res = ""
    while n > 0:
        n, r = divmod(n, 58)
        res = alphabet[r] + res
    return res

# Your final hex key
hex_key = "f8811be90a9d71efe34b3c196e1c92e44aa9e67a7e2f6aa52e39dfe3de4173fb"
key_bytes = bytes.fromhex(hex_key)

# 1. Add 0x80 prefix for Mainnet
# 2. Add 0x01 suffix for Compressed
extended = b'\x80' + key_bytes + b'\x01'

# 3. Double SHA-256 Checksum
h1 = hashlib.sha256(extended).digest()
h2 = hashlib.sha256(h1).digest()
final_key = extended + h2[:4]

# 4. Base58 Encode
wif = base58_encode(final_key)
print(f"Compressed WIF: {wif}")