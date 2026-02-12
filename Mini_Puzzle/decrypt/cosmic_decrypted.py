import os

def solve_duality(input_file):
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    with open(input_file, "rb") as f:
        data = f.read()

    print(f"--- Analysis of {input_file} ---")
    print(f"Total Bytes: {len(data)}")
    
    # Try to find a 32-byte Private Key pattern
    if len(data) >= 32:
        print(f"Potential Hex Key: {data[:32].hex()}")
    
    # Check for readable strings
    import re
    text_parts = re.findall(rb'[ -~]{8,}', data)
    if text_parts:
        print("Readable strings found:")
        for part in text_parts:
            print(f"  [>] {part.decode('ascii', errors='ignore')}")
    else:
        print("No plain text found. Data is likely a raw key fragment.")

solve_duality("cosmic_decrypted.bin")