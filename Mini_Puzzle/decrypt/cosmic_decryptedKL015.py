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

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
inv2 = pow(2, -1, N)

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. THE HALVING: Split and halve only the first 16 bytes
# This treats the beginning and end as independent entities
part1_int = int(half_a_hex[:32], 16)
halved_part1 = (part1_int * inv2) % (2**128) # Modularly halve the first 128 bits

# 3. NEED FUNDS TO LIVE: Complete the second 16 bytes with the 1106 salt
# We use the original tail of your fragment but offset by the LUV funds
part2_int = int(half_a_hex[32:], 16)
final_part2 = (part2_int + 1106) % (2**128)

# 4. RECOMBINE: Construct the full 32-byte hex
final_hex = hex(halved_part1)[2:].zfill(32) + hex(final_part2)[2:].zfill(32)

# 5. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Split-Halved WIF: {base58_check_encode(compressed_payload)}")