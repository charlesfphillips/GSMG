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

# 1. FUNDED BEGINNING
# Add 1106 to the fragment before mirroring
frag_int = (int("8badeb454dbeb5d2263d8774b8b24f1b", 16) + 1106)
mirrored_frag = frag_int ^ (2**128 - 1)

# 2. MIRRORED END
txid_int = int("a798905f53fdcadcbd2e2a1e61d23ba6", 16)
mirrored_txid = txid_int ^ (2**128 - 1)

# 3. THE SYMMETRIC JOIN (1jon)
joined_hex = hex(mirrored_frag)[2:].zfill(32) + hex(mirrored_txid)[2:].zfill(32)
joined_int = int(joined_hex, 16)

# 4. THE FINAL HALVING
# Logical shift to align with the 1G vanity target
final_int = joined_int >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Funded Symmetry WIF: {base58_check_encode(compressed_payload)}")