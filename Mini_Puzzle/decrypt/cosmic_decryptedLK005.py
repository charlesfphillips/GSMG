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

# Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# Better Half: The SHA256 of the Bella Ciao target address string
# This follows the "1_1" (One to One) clue
better_half_input = "1Pi36y7LJugXwFNDVjR1p8p5JoB7eN5zSZ"
better_half_hex = hashlib.sha256(better_half_input.encode('utf-8')).hexdigest()

# SECP256K1 Order (The "Boundaries" of the Matrix)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Integer Addition Logic (2 of 2 Multisig hint)
int_a = int(half_a_hex, 16)
int_b = int(better_half_hex, 16)
luv_funds = 1106

# "Build it" - The architectural sum
final_int = (int_a + int_b + luv_funds) % N
final_hex = hex(final_int)[2:].zfill(64)

print(f"Architect Sum WIF: {base58_check_encode('80' + final_hex)}")