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

# 2. Better Half: The Matrix passwords identified in the clues
# These were found in the 'choice' and 'causality' segments of your files
part1 = hashlib.sha256(b"lastwordsbeforearchichoice").digest()
part2 = hashlib.sha256(b"thispassword").digest()

# 3. The LUV 1106 Offset (The 'Funds' needed to 'Live')
# Added as an integer to the final private key sum
luv_offset = 1106

# 4. Calculate the 'Living' Private Key
int_a = int(half_a_hex, 16)
int_b1 = int.from_bytes(part1, 'big')
int_b2 = int.from_bytes(part2, 'big')

# The Formula: (Half A XOR Part 1) + Part 2 + LUV Offset
# This follows the 'Built It' and 'Need Funds' logic from the transactions
final_int = ((int_a ^ int_b1) + int_b2 + luv_offset) % (0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141)
final_hex = hex(final_int)[2:].zfill(64)

print(f"Final Living WIF: {base58_check_encode('80' + final_hex)}")