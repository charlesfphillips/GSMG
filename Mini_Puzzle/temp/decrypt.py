# Decrypt an OpenSSL-style AES-256-CBC file using password 'matrixsumlist'

import base64
import hashlib
from Crypto.Cipher import AES

password = b"matrixsumlist"  # puzzle password

# Read the encrypted file (same one you would pass to openssl -in)
with open("cosmic_duality_real.txt", "rb") as f:
    data = f.read()

# If file is base64 text, decode it first. If it's raw binary, this will fail.
try:
    data = base64.b64decode(data)
except Exception:
    # Probably already raw binary
    pass

if not data.startswith(b"Salted__"):
    raise ValueError("File does not look like an OpenSSL Salted__ blob")

salt = data[8:16]
ciphertext = data[16:]

# Reproduce OpenSSL EVP_BytesToKey with MD5 to derive key and IV
def evp_bytes_to_key(password_bytes, salt_bytes, key_len=32, iv_len=16):
    d = b""
    while len(d) < key_len + iv_len:
        d = d + hashlib.md5(d + password_bytes + salt_bytes).digest()
    key = d[:key_len]
    iv = d[key_len:key_len + iv_len]
    return key, iv

key, iv = evp_bytes_to_key(password, salt)

cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext_padded = cipher.decrypt(ciphertext)

# Remove PKCS7 padding
pad_len = plaintext_padded[-1]
plaintext = plaintext_padded[:-pad_len]

# Save and print a preview
with open("answer3_2.txt", "wb") as f:
    f.write(plaintext)

print("Decrypted answer written to answer3_2.txt")
print("Preview:")
print(plaintext[:400].decode("utf-8", errors="replace"))