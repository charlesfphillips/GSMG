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

# 1. THE TREASURY SCALAR FROM KL080
scalar_hex = "a0f31c7f56ae7f79476d4e28d5095afc64ca55bd5cb7e885c8aab56002f5eead"

# 2. THE BEGINNING AND THE END SWAP (128-bit swap)
beginning = scalar_hex[:32]
end = scalar_hex[32:]
mirrored_scalar = end + beginning

print(f"Mirrored Treasury Scalar: {mirrored_scalar}")
print("-" * 30)
print(f"Compressed WIF: {base58_check_encode('80' + mirrored_scalar + '01')}")
print(f"Uncompressed WIF: {base58_check_encode('80' + mirrored_scalar)}")