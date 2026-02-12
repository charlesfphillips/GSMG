import hashlib
import binascii

def base58_check_encode(hex_payload):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    raw_bin = binascii.unhexlify(hex_payload)
    # Double SHA256 for the checksum
    digest1 = hashlib.sha256(raw_bin).digest()
    digest2 = hashlib.sha256(digest1).digest()
    final_bin = raw_bin + digest2[:4]
    # Convert to Base58
    num = int(final_bin.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# Half A from your terminal decryption 
half_a = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# The "Better Half" found in the Bella Ciao archive metadata
# This is the SHA-256 of the string "BellaCiao1_1"
better_half = hashlib.sha256(b"BellaCiao1_1").hexdigest()

# Perform the Cosmic Duality XOR
raw_a = binascii.unhexlify(half_a)
raw_b = binascii.unhexlify(better_half)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

# 80 is the prefix for Mainnet Private Keys
print(f"Final Solution WIF: {base58_check_encode('80' + merged)}")