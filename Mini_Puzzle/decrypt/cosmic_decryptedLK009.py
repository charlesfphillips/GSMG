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
int_a = int(half_a_hex, 16)

# The SECP256K1 Curve Order (The limit of all BTC private keys)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# LUV 1106: The "Funds"
funds = 1106

# The "Living" Key: Adding the funds to the fragment
# We test both adding and subtracting (the 'Duality')
final_int_plus = (int_a + funds) % N
final_int_minus = (int_a - funds) % N

print(f"Funds Added WIF: {base58_check_encode('80' + hex(final_int_plus)[2:].zfill(64))}")
print(f"Funds Subtracted WIF: {base58_check_encode('80' + hex(final_int_minus)[2:].zfill(64))}")