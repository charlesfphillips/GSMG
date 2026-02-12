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

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# 1. THE DECRYPTED SOURCE (From your AES success)
full_key_hex = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"

# 2. THE "BETTER HALF" CLUE (N0EHalf XOR BetterHalf)
half1 = int(full_key_hex[:32], 16)
half2 = int(full_key_hex[32:], 16)
unified_half = half1 ^ half2

# 3. THE "BELLA CIAO" CONSTRUCTION
# Using the unified half to fill both sides of the 256-bit scalar
final_scalar_hex = hex(unified_half)[2:].zfill(32) + hex(unified_half)[2:].zfill(32)
final_int = int(final_scalar_hex, 16)

# 4. THE 666 TRANSFORMATION (From the .00000666 BTC clue)
# Applying the "Devil's" shift from the transactions
final_int = (final_int ^ 666)

# 5. THE 1106 FUNDING (The Final Agreement)
final_int = (final_int + 1106) % N
final_hex = hex(final_int)[2:].zfill(64)

# 6. Generate Compressed WIF
compressed_payload = '80' + final_hex + '01'
print(f"Bella Ciao WIF: {base58_check_encode(compressed_payload)}")