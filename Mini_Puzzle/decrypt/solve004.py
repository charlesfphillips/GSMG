import binascii
import hashlib
import re
import base64
from Crypto.Cipher import AES

# PHASE 5: VERIFIED PARAMETERS
PHASE5_KEY_HEX = "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23"
PHASE5_IV_HEX  = "c6ff2e39d98843bc3c26b8a33a15b5c9"
INPUT_FILE     = "cosmic_duality_content.txt"

def hex_to_wif(priv_hex, compressed=True):
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

def solve_phase_5_v2():
    key = binascii.unhexlify(PHASE5_KEY_HEX)
    iv = binascii.unhexlify(PHASE5_IV_HEX)
    
    try:
        with open(INPUT_FILE, "r") as f:
            raw_content = f.read().strip().replace('"', '').replace("'", "")
        
        # Determine if it's Base64 or Hex
        try:
            encrypted_data = base64.b64decode(raw_content)
            print(f"[+] Base64 decoding successful. Binary size: {len(encrypted_data)} bytes.")
        except:
            encrypted_data = binascii.unhexlify(raw_content)
            print(f"[+] Hex decoding successful. Binary size: {len(encrypted_data)} bytes.")

        # Final check for 16-byte boundary
        if len(encrypted_data) % 16 != 0:
            print(f"[!] Warning: Data size ({len(encrypted_data)}) is still not a multiple of 16.")
            print("Truncating/Padding to force attempt...")
            encrypted_data = encrypted_data[:(len(encrypted_data) // 16) * 16]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_raw = cipher.decrypt(encrypted_data)
        
        # Try to unpad or just decode
        try:
            # Manually checking PKCS7 padding
            pad_len = decrypted_raw[-1]
            if 0 < pad_len <= 16:
                plaintext = decrypted_raw[:-pad_len]
            else:
                plaintext = decrypted_raw
        except:
            plaintext = decrypted_raw

        decoded_text = plaintext.decode("utf-8", errors="ignore").strip()
        
        print("\n" + "="*60)
        print("PHASE 5 RESULT:")
        print("="*60)
        print(decoded_text)
        print("="*60)
        
        # Check for 64-char Hex Key
        keys = re.findall(r'[0-9a-fA-F]{64}', decoded_text)
        if keys:
            for k in keys:
                print(f"\n[!!!] TREASURY KEY FOUND: {k}")
                print(f"      WIF (Compressed): {hex_to_wif(k, True)}")
        else:
            print("\n[?] No hex key found. Applying 'HASHTHETEXT' logic...")
            final_secret = hashlib.sha256(decoded_text.encode()).hexdigest()
            print(f"SHA256 of text: {final_secret}")
            print(f"Potential WIF:  {hex_to_wif(final_secret, True)}")

    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    solve_phase_5_v2()