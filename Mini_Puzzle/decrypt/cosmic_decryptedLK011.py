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
raw_a = binascii.unhexlify(half_a_hex)

# 2. The LUV 1106 TXID
txid = "a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383"

# 3. Process the TXID through Hash160 (Bella Ciao Address logic)
sha256_txid = hashlib.sha256(binascii.unhexlify(txid)).digest()
ripemd_txid = hashlib.new('ripemd160', sha256_txid).hexdigest()

# 4. Apply "Funds" Padding (1106 -> 0452)
# We fill the 12-byte gap (24 hex chars) using the LUV funds
padding = "0452" * 6
better_half_32 = ripemd_txid + padding

# 5. XOR Duality
raw_b = binascii.unhexlify(better_half_32)
merged = bytes([a ^ b for a, b in zip(raw_a, raw_b)]).hex()

print(f"TXID Hash160 XOR WIF: {base58_check_encode('80' + merged)}")