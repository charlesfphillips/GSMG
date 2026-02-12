import hashlib
import binascii

# THE SYMMETRIC MIDPOINT (From soln006.py - the one that hit 1G)
MIDPOINT_INT = 0xa181a9a2f28f436b3c2c82833670d72cf5ca021d82bf6ea2f0b58c2f94364a94
# THE SIGNPOST MASK
MASK_INT = int("844e86a69a04eea672049e0e0e8612", 16)
# SECP256K1 ORDER
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def b58check(payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    num = int((payload + chk).hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# 1. THE OFFSET (Duality of the Signpost)
# We test both Addition and Subtraction of the mask from the midpoint
offset_add = (MIDPOINT_INT + MASK_INT) % N
offset_sub = (MIDPOINT_INT - MASK_INT) % N

print(f"--- OFFSET A (Midpoint + Mask) ---")
scalar_a = hex(offset_add)[2:].zfill(64)
print(f"WIF: {b58check(binascii.unhexlify('80' + scalar_a))}")

print(f"\n--- OFFSET B (Midpoint - Mask) ---")
scalar_b = hex(offset_sub)[2:].zfill(64)
print(f"WIF: {b58check(binascii.unhexlify('80' + scalar_b))}")