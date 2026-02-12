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

# 1. Half A: Your decrypted fragment (Take first 16 bytes)
half_a_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
raw_a_16 = binascii.unhexlify(half_a_hex[:32])

# 2. Better Half: The LUV 1106 TXID (Take first 16 bytes)
txid = "a798905f53fdcadcbd2e2a1e61d23ba69a07e26130a78c76da4bf4d7a170f383"
raw_tx_16 = binascii.unhexlify(txid[:32])

# 3. THE HALVING: XOR the two halves together
xor_half = bytes([a ^ b for a, b in zip(raw_a_16, raw_tx_16)])

# 4. NEED FUNDS TO LIVE: Complete the 32-byte key
# Use the hex value of 1106 (0452) padded to 16 bytes as the 'Life' tail
tail = binascii.unhexlify("00000000000000000000000000000452")
final_key = xor_half + tail

# 5. Generate Compressed K/L WIF
compressed_payload = '80' + final_key.hex() + '01'

print(f"Multisig Halved WIF: {base58_check_encode(compressed_payload)}")