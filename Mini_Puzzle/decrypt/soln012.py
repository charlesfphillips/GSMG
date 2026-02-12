###############################################################################
# 5) FINAL EXECUTION BLOCK: THE NESTED DECRYPTION & WIF RECOVERY
###############################################################################

def hex_to_wif(priv_hex, compressed=True):
    """Converts a raw hex private key to Bitcoin WIF format."""
    prefix = b'\x80'
    suffix = b'\x01' if compressed else b''
    data = prefix + binascii.unhexlify(priv_hex) + suffix
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    
    # Base58 Encoding
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = int.from_bytes(data + checksum, 'big')
    res = ""
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

def finalize_puzzle(b64_ciphertext):
    # The GSMG IV found in the OP_RETURN/Notes
    iv_final = "566e59af68feda0a0d8f09610f8d8424"
    
    print("\n[+] Attempting Final Decryption...")
    try:
        # We use the Master Key we derived in Section 1
        plaintext = decrypt_cosmic_duality(b64_ciphertext, master_key_hex, iv_final)
        decoded_text = plaintext.decode("utf-8", errors="ignore").strip()
        
        print("-" * 50)
        print("DECRYPTED CONTENT REVEALED:")
        print(decoded_text)
        print("-" * 50)
        
        # Look for a 64-character hex string in the output
        import re
        potential_keys = re.findall(r'[0-9a-fA-F]{64}', decoded_text)
        
        if potential_keys:
            print(f"\n[!] Found {len(potential_keys)} potential private key(s).")
            for key in potential_keys:
                print(f"Hex: {key}")
                print(f"WIF (Compressed):   {hex_to_wif(key, True)}")
                print(f"WIF (Uncompressed): {hex_to_wif(key, False)}")
        else:
            print("\n[?] No hex key found in plaintext. Check if the output is a seed phrase.")

    except Exception as e:
        print(f"\n[!] Error during finalization: {e}")
        print("Tip: Ensure the b64_ciphertext includes the 'Salted__' header after decoding.")

# --- PLACE YOUR ENCRYPTED DATA HERE ---
# Example: Using a dummy string. Replace with the actual contents of your .txt file.
if __name__ == "__main__":
    # If you have a file named 'cosmic_duality.txt', uncomment the following:
    # with open("cosmic_duality.txt", "r") as f:
    #     cipher_input = f.read().strip()
    # finalize_puzzle(cipher_input)
    
    print("\nScript Ready. Provide the Base64 ciphertext to the 'finalize_puzzle' function.")