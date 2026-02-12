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

# 1. THE DUALITY SPLIT
# Mirror only the fragment (The Beginning)
frag_int = int("8badeb454dbeb5d2263d8774b8b24f1b", 16)
mirrored_frag = frag_int ^ (2**128 - 1)

# Keep the TXID constant (The Better Half / The End)
txid_hex = "a798905f53fdcadcbd2e2a1e61d23ba6"

# 2. THE JOIN (1jon)
# Combine the mirrored beginning with the original end
joined_int = int(hex(mirrored_frag)[2:].zfill(32) + txid_hex, 16)

# 3. THE FINAL SHIFT
# Apply the logical shift that produced the 1G markers
final_int = (joined_int ^ 1106) >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Split-Mirror WIF: {base58_check_encode(compressed_payload)}")