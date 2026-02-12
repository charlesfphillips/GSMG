import binascii

def analyze_and_xor(filename):
    with open(filename, "rb") as f:
        data = f.read()

    # 1. Check for readable text hidden in the binary 
    import re
    strings = re.findall(rb'[ -~]{6,}', data)
    print("--- Found Strings ---")
    for s in strings:
        print(s.decode('ascii'))

    # 2. Extract the First 32 Bytes (Potential Raw Private Key)
    # Bitcoin private keys are 32 bytes.
    if len(data) >= 32:
        potential_hex = binascii.hexlify(data[:32]).decode()
        print(f"\n--- Potential Private Key Fragment (Hex) ---\n{potential_hex}")

    # 3. Attempt common XOR with 'theone' or 'matrixsumlist'
    # These tokens were identified as part of the strategy.
    key = b"theone" 
    xor_result = bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    
    with open("xor_output.bin", "wb") as f:
        f.write(xor_result)
    print("\n--- XOR operation with 'theone' saved to xor_output.bin ---")

analyze_and_xor("cosmic_decrypted.bin")