import hashlib
import binascii
import hmac

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

# 1. THE 512-BIT DUALITY SEED
k1 = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
k2 = "a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2"
seed_512 = k1 + k2 

# 2. BIP-32 MASTER KEY DERIVATION
# The "Spoon" is the HMAC-SHA512 using "Bitcoin seed" as the key
hash_512 = hmac.new(b"Bitcoin seed", binascii.unhexlify(seed_512), hashlib.sha512).digest()
master_priv = hash_512[:32].hex()

print(f"Master Reward Scalar: {master_priv}")
print("-" * 30)
# Testing Uncompressed (Signpost format) and Compressed (Standard HD format)
print(f"Uncompressed WIF: {base58_check_encode('80' + master_priv)}")
print(f"Compressed WIF:   {base58_check_encode('80' + master_priv + '01')}")