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

# 2. Better Half: The TXID of the "1106" Transaction (Message 14)
txid_better_half = "a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383"

# 3. Perform the XOR (The "Duality" of the two halves)
raw_a = binascii.unhexlify(half_a_hex)
raw_b = binascii.unhexlify(txid_better_half)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

# 4. Generate the WIF
print(f"TXID Duality WIF: {base58_check_encode('80' + merged)}")