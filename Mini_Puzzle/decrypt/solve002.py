import hashlib
import binascii
import base64
import re
from Crypto.Cipher import AES

# ... (Keep your decrypt_openssl_salted and hex_to_wif functions) ...

def finalize_puzzle_v4(filename):
    # TOKENS as a Newline-separated string (Common in "list" puzzles)
    tokens = [
        "matrixsumlist", "enter", "lastwordsbeforearchichoice",
        "thispassword", "matrixsumlist", "sha256", "theone"
    ]
    newline_pass = "\n".join(tokens)
    
    # THE MASK (The "Signpost" from the OP_RETURN)
    mask_str = "844e86a69a04eea672049e0e0e8612"
    mask_bin = binascii.unhexlify(mask_str)
    
    # POTENTIAL KEYS
    potential_keys = [
        ("Newline Passphrase", hashlib.sha256(newline_pass.encode()).digest()),
        ("Mask as Passphrase", mask_str.encode()), # OpenSSL will hash this with salt
        ("Mask as Raw Key", hashlib.sha256(mask_bin).digest()),
        ("TheOne SHA256", hashlib.sha256(b"theone").digest())
    ]

    try:
        with open(filename, "r") as f:
            b64_data = f.read().strip().replace('"', '').replace("'", "")
        cipher_bytes = base64.b64decode(b64_data)
    except:
        print("[-] Error reading file.")
        return

    for name, key_material in potential_keys:
        print(f"\n[?] Testing: {name}")
        # Try Classical OpenSSL (Passphrase -> KDF)
        try:
            # For "Mask as Passphrase", we use it to derive key/iv from salt
            pt = decrypt_openssl_salted(cipher_bytes, key_material, iv_bytes=None)
            print(f"✅ SUCCESS! {name} worked with Standard KDF.")
            process_plaintext(pt)
            return
        except:
            pass
            
        # Try Raw Binary Key (Manual IV)
        try:
            iv = binascii.unhexlify("566e59af68feda0a0d8f09610f8d8424")
            # If key_material is already 32 bytes, use it. Else hash it.
            key = key_material if len(key_material) == 32 else hashlib.sha256(key_material).digest()
            pt = decrypt_openssl_salted(cipher_bytes, key, iv_bytes=iv)
            print(f"✅ SUCCESS! {name} worked with Known IV.")
            process_plaintext(pt)
            return
        except:
            continue
            
    print("\n[-] All attempts failed. Check if 'matrixsumlist' is a filename in your folder.")

if __name__ == "__main__":
    finalize_puzzle_v4("cosmic_duality_content.txt")