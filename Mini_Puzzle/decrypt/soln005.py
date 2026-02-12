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

# 1. THE MASTER SCALAR (From your last run)
master_hex = "3aed6cb4f65a73fb26d75d6754a0022ddf79520d7f731e93688a328c752045c5"
master_int = int(master_hex, 16)

# 2. THE CAUSALITY MASK (OP_RETURN)
# 844e86a69a04eea672049e0e0e8612
mask_hex = "844e86a69a04eea672049e0e0e8612"
mask_int = int(mask_hex, 16)

# 3. THE "NO SPOON" FINAL SYNTHESIS
# We XOR the Master Key with the Mask to find the Treasury
final_scalar_int = master_int ^ mask_int
final_scalar_hex = hex(final_scalar_int)[2:].zfill(64)

print(f"Final Treasury Scalar: {final_scalar_hex}")
print("-" * 30)
# Testing Uncompressed as it matches the 19Av3 signpost format
print(f"Uncompressed WIF: {base58_check_encode('80' + final_scalar_hex)}")
print(f"Compressed WIF:   {base58_check_encode('80' + final_scalar_hex + '01')}")