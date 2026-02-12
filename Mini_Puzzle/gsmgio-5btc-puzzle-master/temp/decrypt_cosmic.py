from Crypto.Cipher import AES
from Crypto.Hash import MD5
import binascii
import base64

# Master key binary (32 bytes)
master_key_bytes = binascii.unhexlify("818af53daa3028449f125a2e4f47259ddf9b9d86e59ce6c4993a67ffd76bb402")

# Read base64 file
with open("cosmic_duality_content.txt", "r") as f:
    base64_data = f.read().replace("\n", "").replace(" ", "")

ciphertext = base64.b64decode(base64_data)

# Extract salt (bytes 8-16)
salt = ciphertext[8:16]  # Should be b'\x2d\x3f\x6f\xe0\x6d\xc9\x50\xe6'

# EVP_BytesToKey MD5 implementation (no iterations, chained MD5)
def evp_bytes_to_key(password, salt, key_len=32, iv_len=16):
    d = b''
    d_i = b''
    while len(d) < key_len + iv_len:
        d_i = MD5.new(d_i + password + salt).digest()
        d += d_i
    key = d[:key_len]
    iv = d[key_len:key_len + iv_len]
    return key, iv

derived_key, derived_iv = evp_bytes_to_key(master_key_bytes, salt)

print("Derived Key (hex):", derived_key.hex())
print("Derived IV (hex):", derived_iv.hex())

# Decrypt
cipher = AES.new(derived_key, AES.MODE_CBC, derived_iv)
plaintext = cipher.decrypt(ciphertext[16:])  # Skip Salted__ + salt

# Remove PKCS#7 padding
pad_len = plaintext[-1]
plaintext = plaintext[:-pad_len]

print("\nDecrypted (first 500 chars):")
print(plaintext.decode('utf-8', errors='ignore')[:500])
print("\nFull length:", len(plaintext))

# Save full
with open("cosmic_decrypted.txt", "wb") as f:
    f.write(plaintext)