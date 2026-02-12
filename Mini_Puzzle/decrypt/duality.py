import hashlib
import binascii

# secp256k1 curve order
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Verified coordinates from prior successful decryption
K1 = 0x8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af
K2 = 0xa986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2

# Clues extracted from transactions.txt
MASK_HEX = "844e86a69a04eea672049e0e0e8612" # 
LUV_ITERATIONS = 1106                      # 
SALT = b"women"                            # 

def bit_rotate_left(val, n, bits=256):
    """♀ Symbol Logic: 12-bit circular rotation."""
    return ((val << n) & ((1 << bits) - 1)) | (val >> (bits - n))

def base58_check_encode(hex_data):
    data = binascii.unhexlify(hex_data)
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    combined = data + checksum
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int.from_bytes(combined, 'big')
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# STEP 1: Duality XOR (The 'Half and Better Half' )
combined_secret = K1 ^ K2

# STEP 2: Apply the 15-byte rolling mask 
mask_bytes = binascii.unhexlify(MASK_HEX)
secret_bytes = binascii.unhexlify(hex(combined_secret)[2:].zfill(64))
full_mask = (mask_bytes * 3)[:32]
masked_val = bytes(a ^ b for a, b in zip(secret_bytes, full_mask))

# STEP 3: Hashing Loop with "women" salt [cite: 12, 14]
current_data = masked_val + SALT
for _ in range(LUV_ITERATIONS):
    current_data = hashlib.sha256(current_data).digest()

# STEP 4: Apply 12-bit Shift (♀ Instruction )
loop_result = int.from_bytes(current_data, 'big')
final_scalar = bit_rotate_left(loop_result, 12) % N
final_hex = hex(final_scalar)[2:].zfill(64)

# STEP 5: Generate WIF (Compressed)
wif = base58_check_encode('80' + final_hex + '01')

print(f"Final WIF for 1GSMG...: {wif}")