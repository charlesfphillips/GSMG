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

# 1. Half A: Your beginning (first 16 bytes)
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1b" # First 32 chars

# 2. The Better Half: The LUV 1106 TXID (first 16 bytes)
# TXID: a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383
better_half_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"

# 3. DUALITY: Concatenate them to form the 32-byte Private Key
final_hex = half_a_hex + better_half_hex

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Hybrid Concatenated WIF: {base58_check_encode(compressed_payload)}")