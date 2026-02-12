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

# 1. Fragment & TXID Duality
raw_a = binascii.unhexlify("8badeb454dbeb5d2263d8774b8b24f1b")
raw_tx = binascii.unhexlify("a798905f53fdcadcbd2e2a1e61d23ba6")

# 2. XOR to create the base scalar
xor_half = bytes([a ^ b for a, b in zip(raw_a, raw_tx)])
base_int = int(xor_half.hex() + "00000000000000000000000000000452", 16)

# 3. FINAL HALVING: Multiply the entire 32-byte scalar by inv2
final_int = (base_int * inv2) % N
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Agreement Halved WIF: {base58_check_encode(compressed_payload)}")