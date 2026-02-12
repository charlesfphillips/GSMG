import hashlib
import binascii

# YOUR CORE COMPONENTS
K1_HEX = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
K2_HEX = "a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2"
MASK_HEX = "844e86a69a04eea672049e0e0e8612"

def xor_hex_strings(s1, s2):
    """XOR two hex strings, looping the shorter one (s2) if necessary."""
    b1 = binascii.unhexlify(s1)
    b2 = binascii.unhexlify(s2)
    # Loop b2 to match length of b1
    b2_looped = (b2 * (len(b1) // len(b2) + 1))[:len(b1)]
    return bytes(a ^ b for a, b in zip(b1, b2_looped)).hex()

def get_wif_and_addr(scalar_hex):
    # Pure Python Base58 Check
    def b58check(payload):
        alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
        chk = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
        num = int((payload + chk).hex(), 16)
        res = ''
        while num > 0:
            num, rem = divmod(num, 58)
            res = alphabet[rem] + res
        return res

    # WIF Uncompressed
    wif = b58check(binascii.unhexlify('80' + scalar_hex))
    return wif

# THE "TURING" TRANSFORM
# Apply the looping mask to the Better Half (k2)
transformed_k2 = xor_hex_strings(K2_HEX, MASK_HEX)

print(f"--- THE TRANSCENDED RESULT ---")
print(f"Original k2:    {K2_HEX}")
print(f"Transformed k2: {transformed_k2}")
print(f"Uncompressed WIF: {get_wif_and_addr(transformed_k2)}")