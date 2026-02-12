import hashlib
import binascii

# DATA
K2_HEX = "a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2"
MASK_HEX = "844e86a69a04eea672049e0e0e8612"
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def xor_hex_strings(s1, s2):
    b1 = binascii.unhexlify(s1)
    b2 = binascii.unhexlify(s2)
    b2_looped = (b2 * (len(b1) // len(b2) + 1))[:len(b1)]
    return bytes(a ^ b for a, b in zip(b1, b2_looped)).hex()

def ror12(val):
    return ((val >> 12) | (val << (256 - 12))) & (2**256 - 1)

def b58check(payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    num = int((payload + chk).hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# 1. XOR Transform
xor_result_hex = xor_hex_strings(K2_HEX, MASK_HEX)
xor_result_int = int(xor_result_hex, 16)

# 2. Circular Rotation (The Female ♀ 12-bit Shift)
final_scalar_int = ror12(xor_result_int) % N
final_scalar_hex = hex(final_scalar_int)[2:].zfill(64)

print(f"Final Combined Scalar: {final_scalar_hex}")
print("-" * 40)
print(f"Uncompressed WIF: {b58check(binascii.unhexlify('80' + final_scalar_hex))}")
print(f"Compressed WIF:   {b58check(binascii.unhexlify('80' + final_scalar_hex + '01'))}")