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

# 1. Your Decrypted Half A
half_a = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. The "Better Half" (RIPEMD-160 of the Bella Ciao address)
# Address: 1Pi36y7LJugXwFNDVjR1p8p5JoB7eN5zSZ
address_hash = "f69542a4a75e2f16a13d76e4c34a2c53a812e5c6"

# 3. Apply the LUV 1106 Transformation
# 1106 is the salt; we pad the address hash to 32 bytes using the salt
better_half = address_hash + "000000000000000000000000" + "1106"

# 4. Perform XOR
raw_a = binascii.unhexlify(half_a)
raw_b = binascii.unhexlify(better_half)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

# 5. Generate WIF
print(f"Final WIF: {base58_check_encode('80' + merged)}")