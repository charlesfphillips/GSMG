import binascii
import hashlib
import re
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

# PHASE 5: VERIFIED PARAMETERS
PHASE5_KEY_HEX = "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23"
PHASE5_IV_HEX  = "c6ff2e39d98843bc3c26b8a33a15b5c9"
INPUT_FILE     = "cosmic_duality_content.txt"

def hex_to_wif(priv_hex, compressed=True):
    """Converts the raw secret to a spendable Bitcoin WIF."""
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

def solve_phase_5():
    key = binascii.unhexlify(PHASE5_KEY_HEX)
    iv = binascii.unhexlify(PHASE5_IV_HEX)
    
    try:
        with open(INPUT_FILE, "rb") as f:
            # We treat the file as raw binary data now
            encrypted_data = f.read()
            
        print(f"[+] Decrypting {len(encrypted_data)} bytes...")
        cipher = AES.new(key, AES.MODE_CBC, iv)
        
        # Decrypt and attempt to unpad (PKCS7)
        decrypted_raw = cipher.decrypt(encrypted_data)
        
        try:
            plaintext = unpad(decrypted_raw, AES.block_size)
        except ValueError:
            print("[!] Warning: Padding check failed. Outputting raw data.")
            plaintext = decrypted_raw

        decoded_text = plaintext.decode("utf-8", errors="ignore")
        
        print("\n" + "="*60)
        print("BRIDGE COLLAPSED: REVEALED CONTENT")
        print("="*60)
        print(decoded_text)
        print("="*60)
        
        # Search for the Private Key (64-char Hex or WIF patterns)
        keys = re.findall(r'[0-9a-fA-F]{64}', decoded_text)
        if keys:
            for k in keys:
                print(f"\n[!!!] TREASURY KEY FOUND: {k}")
                print(f"      Legacy WIF: {hex_to_wif(k, False)}")
                print(f"      SegWit WIF: {hex_to_wif(k, True)}")
        else:
            print("\n[?] No direct hex key found. Look for a BIP39 mnemonic in the text.")

    except Exception as e:
        print(f"[-] Execution Error: {e}")

if __name__ == "__main__":
    solve_phase_5()