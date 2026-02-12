import subprocess
import os
import concurrent.futures

# The encrypted file
INPUT_FILE = "cosmic_duality_real_CORRECT.txt"

# Passwords found in your search results
passwords = [
    "matrixsumlist", "theseedisplanted", "ciao Bella", "fans",
    "theflowerblossomsthroughwhatseemstobeaconcretesurface",
    "98", "1701", "2440", "277", "948", "Turing Complete.",
    "matrixsumlistenter", "HALFANDBETTERHALF", "werner", "matrix"
]

# Hex keys/IVs found in your search results
hex_configs = [
    {
        "K": "6ac438facf366702b60d6dfcebd39815b582f19b591b3fdf69240c6966f4fc23",
        "iv": "c6ff2e39d98843bc3c26b8a33a15b5c9"
    }
]

def try_decrypt(pwd, md_type, pbkdf2=False):
    out_file = f"dec_{md_type}_{'pbkdf2_' if pbkdf2 else ''}{pwd[:10]}.bin"
    
    cmd = ["openssl", "enc", "-aes-256-cbc", "-d", "-a", "-A", "-in", INPUT_FILE, "-out", out_file]
    
    if pbkdf2:
        cmd.append("-pbkdf2")
    
    cmd.extend(["-md", md_type, "-pass", f"pass:{pwd}"])

    try:
        # Run command, suppress stderr (the 'bad decrypt' messages)
        result = subprocess.run(cmd, capture_output=True, timeout=5)
        
        if os.path.exists(out_file) and os.path.getsize(out_file) > 0:
            # Check for "Salted__" header (53 61 6c 74 65 64 5f 5f)
            with open(out_file, 'rb') as f:
                header = f.read(8)
                if header != b'Salted__':
                    print(f"[*] SUCCESS? Found file: {out_file} (Pass: {pwd}, MD: {md_type})")
                    return True
        if os.path.exists(out_file): os.remove(out_file)
    except:
        pass
    return False

def try_hex_key(k, iv):
    out_file = "dec_hex_key.bin"
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-d", "-a", "-A", 
        "-in", INPUT_FILE, "-K", k, "-iv", iv, "-out", out_file
    ]
    subprocess.run(cmd, capture_output=True)
    if os.path.exists(out_file) and os.path.getsize(out_file) > 100:
        print(f"[!!!] SUCCESS with HEX KEY: {out_file}")

if __name__ == "__main__":
    print("--- Starting Multicore Decryption Scan ---")
    
    # Try the Hex Key first
    for cfg in hex_configs:
        try_hex_key(cfg["K"], cfg["iv"])

    # Try all passwords with different MDs and PBKDF2
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        for p in passwords:
            for md in ["md5", "sha256"]:
                executor.submit(try_decrypt, p, md, False)
                executor.submit(try_decrypt, p, md, True)

    print("--- Scan Finished ---")