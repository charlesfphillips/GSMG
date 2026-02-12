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

# Half A: The fragment you have
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# Testing the "LUV 1106" string as the Better Half
# We will test common variations of the hint string
hints = ["LUV 1106", "1106", "luv 1106", "LUV1106"]

print("--- Testing LUV 1106 XOR Duality ---")
for hint in hints:
    better_half = hashlib.sha256(hint.encode('utf-8')).hexdigest()
    raw_a = binascii.unhexlify(half_a_hex)
    raw_b = binascii.unhexlify(better_half)
    merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()
    
    print(f"Hint: '{hint}' -> WIF: {base58_check_encode('80' + merged)}")