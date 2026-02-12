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
int_a = int(half_a_hex, 16)

# 2. NEED FUNDS TO LIVE: Add the 1106 satoshis first
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
living_key = (int_a + 1106) % N

# 3. THE HALVING: Right-shift the entire living key by 1 bit
final_int = living_key >> 1
final_hex = hex(final_int)[2:].zfill(64)

# 4. Generate Compressed K/L WIF
compressed_payload = '80' + final_hex + '01'

print(f"Pre-Shift Funded WIF: {base58_check_encode(compressed_payload)}")