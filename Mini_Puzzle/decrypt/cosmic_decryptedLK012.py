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

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. Better Half: The LUV 1106 TXID (Message 14)
txid = "a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383"

# 3. The "Halving" - Concatenate 16 bytes of each
# Taking the first 32 hex chars (16 bytes) of each
merged_hex = half_a_hex[:32] + txid[:32]

print(f"Concatenated WIF: {base58_check_encode('80' + merged_hex)}")

# Alternative: Reversed Concatenation (Better Half + Half A)
merged_hex_alt = txid[:32] + half_a_hex[:32]
print(f"Reversed Concatenated WIF: {base58_check_encode('80' + merged_hex_alt)}")