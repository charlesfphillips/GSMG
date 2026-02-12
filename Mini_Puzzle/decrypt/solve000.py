import hashlib
import binascii
import base64
import re
from functools import reduce
from Crypto.Cipher import AES

###############################################################################
# 1) MASTER KEY DERIVATION
###############################################################################
TOKENS = [
    "matrixsumlist",
    "enter",
    "lastwordsbeforearchichoice",
    "thispassword",
    "matrixsumlist",  # repeated
    "sha256",
    "theone",
]

def sha256_bytes(s):
    return hashlib.sha256(s.encode("utf-8")).digest()

def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def derive_master_key_from_tokens(tokens):
    hashes = [sha256_bytes(t) for t in tokens]
    key = reduce(xor_bytes, hashes)
    return key

###############################################################################
# 2) DECRYPTION UTILITIES
###############################################################################
def openssl_bytes_to_key(password_bytes, salt, key_len=32, iv_len=16):
    """Replicates OpenSSL EVP_BytesToKey (MD5) derivation."""
    out = b""
    prev = b""
    while len(out) < (key_len + iv_len):
        prev = hashlib.md5(prev + password_bytes + salt).digest()
        out += prev
    return out[:key_len], out[key_len:key_len+iv_len]

def hex_to_wif(priv_hex, compressed=True):
    """Converts raw hex to Bitcoin Wallet Import Format."""
    prefix = b'\x80'
    suffix = b'\x01' if compressed else b''
    data = prefix + binascii.unhexlify(priv_hex) + suffix
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(data + checksum, 'big')
    res = ""
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

def decrypt_openssl_salted(cipher_bytes, key_bytes, iv_bytes=None):
    """Attempts to decrypt the Salted__ blob."""
    if not cipher_bytes.startswith(b"Salted__"):
        raise ValueError("Ciphertext does not start with 'Salted__' header")

    salt = cipher_bytes[8:16]
    enc = cipher_bytes[16:]

    # If iv_bytes is provided, use it. Otherwise, derive from salt (Classic OpenSSL).
    if iv_bytes is None:
        _, iv = openssl_bytes_to_key(key_bytes, salt)
    else:
        iv = iv_bytes

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(enc)

    # PKCS#7 unpad
    pad_len = plaintext_padded[-1]
    if pad_len <= 0 or pad_len > 16:
        raise ValueError("Padding check failed (wrong key or IV)")
    return plaintext_padded[:-pad_len]

###############################################################################
# 3) FINAL HARNESS
###############################################################################
def finalize_puzzle(filename):
    master_key = derive_master_key_from_tokens(TOKENS)
    print(f"[+] Derived Master Key: {master_key.hex()}")
    
    # IV from your notes
    known_iv_hex = "566e59af68feda0a0d8f09610f8d8424"
    known_iv = binascii.unhexlify(known_iv_hex)

    try:
        with open(filename, "r") as f:
            b64_data = f.read().strip().replace('"', '').replace("'", "")
        cipher_bytes = base64.b64decode(b64_data)
    except Exception as e:
        print(f"[-] File Error: {e}")
        return

    print(f"[+] Loaded Ciphertext ({len(cipher_bytes)} bytes)")
    
    # ATTEMPT 1: Using specific Known IV
    print("\n[?] Attempting decryption with Known IV...")
    try:
        pt = decrypt_openssl_salted(cipher_bytes, master_key, iv_bytes=known_iv)
        process_plaintext(pt)
        return
    except Exception as e:
        print(f"    Failed: {e}")

    # ATTEMPT 2: Using KDF Derived IV (Classical OpenSSL)
    print("\n[?] Attempting decryption with Derived IV (Standard OpenSSL)...")
    try:
        pt = decrypt_openssl_salted(cipher_bytes, master_key, iv_bytes=None)
        process_plaintext(pt)
    except Exception as e:
        print(f"    Failed: {e}")

def process_plaintext(pt):
    decoded = pt.decode("utf-8", errors="ignore").strip()
    print("\n" + "="*50)
    print("DECRYPTED SUCCESS:")
    print(decoded)
    print("="*50)
    
    keys = re.findall(r'[0-9a-fA-F]{64}', decoded)
    if keys:
        for k in keys:
            print(f"\n[!] RECOVERED PRIVATE KEY: {k}")
            print(f"    WIF (Compressed):   {hex_to_wif(k, True)}")
            print(f"    WIF (Uncompressed): {hex_to_wif(k, False)}")
    else:
        print("\n[-] No hex private key found in text. Check for seed phrases above.")

if __name__ == "__main__":
    # Ensure your file is named 'cosmic_duality_content.txt'
    finalize_puzzle("cosmic_duality_content.txt")