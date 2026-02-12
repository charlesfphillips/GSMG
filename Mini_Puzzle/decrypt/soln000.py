import hashlib
import binascii

def base58_check_encode(hex_payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    raw_bin = binascii.unhexlify(hex_payload)
    digest1 = hashlib.sha256(raw_bin).digest()
    digest2 = hashlib.sha256(digest1).digest()
    final_bin = raw_bin + digest2[:4]
    num = int(final_bin.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# THE "BETTER HALF" COMPONENT
k2_hex = "a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2"

# 1. DIRECT DERIVATION
print(f"Option A: Direct k2 Scalar")
print(f"Compressed WIF: {base58_check_encode('80' + k2_hex + '01')}")
print(f"Uncompressed WIF: {base58_check_encode('80' + k2_hex)}")
print("-" * 30)

# 2. THE HMAC "AGREEMENT" (BellaCiao)
# Using k2 as the secret and "BellaCiao" as the message
passphrase = b"BellaCiao"
k2_bytes = binascii.unhexlify(k2_hex)
hmac_key = hashlib.sha256(k2_bytes + passphrase).hexdigest()

print(f"Option B: HMAC-Transcended Scalar (BellaCiao)")
print(f"Compressed WIF: {base58_check_encode('80' + hmac_key + '01')}")