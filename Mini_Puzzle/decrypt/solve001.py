import hashlib
import binascii
import base64
import re
from Crypto.Cipher import AES

# ... (Keep previous decryption and WIF helper functions) ...

def derive_alternative_keys(tokens):
    # Method A: Concatenated string (Standard GSMG "Passphrase" style)
    concat_str = "".join(tokens)
    key_a = hashlib.sha256(concat_str.encode("utf-8")).digest()
    
    # Method B: Unique XOR (Removing the duplicate)
    unique_tokens = []
    [unique_tokens.append(t) for t in tokens if t not in unique_tokens]
    hashes = [hashlib.sha256(t.encode("utf-8")).digest() for t in unique_tokens]
    from functools import reduce
    key_b = reduce(lambda x, y: bytes(a ^ b for a, b in zip(x, y)), hashes)
    
    return [("Concatenated", key_a), ("Unique XOR", key_b)]

def finalize_puzzle_v2(filename):
    tokens = [
        "matrixsumlist", "enter", "lastwordsbeforearchichoice",
        "thispassword", "matrixsumlist", "sha256", "theone"
    ]
    
    potential_keys = derive_alternative_keys(tokens)
    # Add your original XOR key as well
    orig_hashes = [hashlib.sha256(t.encode("utf-8")).digest() for t in tokens]
    from functools import reduce
    key_orig = reduce(lambda x, y: bytes(a ^ b for a, b in zip(x, y)), orig_hashes)
    potential_keys.append(("Original XOR", key_orig))

    known_iv = binascii.unhexlify("566e59af68feda0a0d8f09610f8d8424")

    try:
        with open(filename, "r") as f:
            b64_data = f.read().strip().replace('"', '').replace("'", "")
        cipher_bytes = base64.b64decode(b64_data)
    except:
        return

    for name, key in potential_keys:
        print(f"\n[?] Testing Key: {name} ({key.hex()[:16]}...)")
        # Try both IV methods for each key
        for iv_type, iv in [("Known IV", known_iv), ("Derived IV", None)]:
            try:
                pt = decrypt_openssl_salted(cipher_bytes, key, iv_bytes=iv)
                print(f"✅ SUCCESS with {name} / {iv_type}!")
                process_plaintext(pt)
                return
            except:
                continue
    print("\n[-] All combinations failed. Checking token content...")

# Replace finalize_puzzle with finalize_puzzle_v2 in your main block
if __name__ == "__main__":
    finalize_puzzle_v2("cosmic_duality_content.txt")