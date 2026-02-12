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

# 2. Better Half: The TXID of the "1106" Transaction
txid = "a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383"

# 3. The Halving: Take 16 bytes (32 hex chars) from each
# This creates a "2 of 2" architectural whole
merged_hex = half_a_hex[:32] + txid[:32]

# 4. Need Funds to Live: Add 1106 to the resulting integer
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
final_int = (int(merged_hex, 16) + 1106) % N
final_hex = hex(final_int)[2:].zfill(64)

print(f"Halved/Funds Merged WIF: {base58_check_encode('80' + final_hex)}")