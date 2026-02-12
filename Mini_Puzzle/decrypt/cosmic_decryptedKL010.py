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

# 1. Half A: Your decrypted fragment
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
int_a = int(half_a_hex, 16)

# 2. LUV 1106: Little-Endian conversion
# 1106 (0x0452) in 8-byte Little-Endian is 5204000000000000
le_funds = int.from_bytes(binascii.unhexlify("5204000000000000"), byteorder='big')

# 3. Final Duality: (Key + LE_Funds) * Inv2
inv2 = pow(2, -1, N)
final_int = ((int_a + le_funds) * inv2) % N
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Final LE-Funded WIF: {base58_check_encode(compressed_payload)}")