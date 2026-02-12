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

# 1. THE LIVE BEGINNING
# Apply 1106 Funds XOR to the fragment first
frag_int = int("8badeb454dbeb5d2263d8774b8b24f1b", 16) ^ 1106

# 2. THE MIRROR (Architect Alignment)
mirrored_frag = frag_int ^ (2**128 - 1)

# 3. THE JOIN (Duality)
txid_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"
joined_int = int(hex(mirrored_frag)[2:].zfill(32) + txid_hex, 16)

# 4. THE FINAL SHIFT (Halving)
final_int = joined_int >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Live-Fragment WIF: {base58_check_encode(compressed_payload)}")