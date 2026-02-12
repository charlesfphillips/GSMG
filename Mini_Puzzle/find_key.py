import re

def find_readable_strings(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    
    # This regex finds sequences of printable ASCII characters
    # We are looking for sequences roughly around 227 characters
    strings = re.findall(b"[\\x20-\\x7E]{100,}", data)
    
    print(f"--- Found {len(strings)} potential long strings ---")
    for i, s in enumerate(strings):
        decoded = s.decode('ascii', errors='ignore')
        print(f"\nString #{i+1} (Length: {len(decoded)}):")
        print(decoded)
        
        if len(decoded) == 227:
            print("!!! MATCH FOUND: THIS IS THE 227-CHARACTER STRING FROM THE CLUE !!!")

find_readable_strings("decrypted_output.bin")