#!/usr/bin/env python3
"""
STEP 3: Decode HEX Sections (a=1-26, o=0 -> hex -> ASCII)
"""
import re

print("="*70)
print("STEP 3: DECODE HEX SECTIONS")
print("="*70)

def decode_hex_section(text):
    """Decode: a=1, b=2, ..., z=26, o=0 -> convert to hex -> ASCII"""
    char_map = {}
    for i in range(26):
        char_map[chr(ord('a') + i)] = str(i + 1)
    char_map['o'] = '0'
    
    # Convert each letter to its number
    num_str = ''.join(char_map.get(c, '') for c in text.lower() if c in char_map)
    
    # Interpret pairs as hex
    result = ""
    for i in range(0, len(num_str) - 1, 2):
        pair = num_str[i:i+2]
        try:
            val = int(pair, 16)
            if 32 <= val <= 126:  # Printable ASCII
                result += chr(val)
        except:
            pass
    return result, num_str

try:
    content = open('salphaseion_content.txt', 'r').read()
    print("\n✓ Opened salphaseion_content.txt")
except FileNotFoundError:
    print("\n✗ ERROR: salphaseion_content.txt not found!")
    exit(1)

# Remove spaces and find letter sequences
content_nospace = content.replace(' ', '')

# Find sections that look like hex (a=1-26, o=0)
print("\nSearching for HEX sections (a=1-26, o=0)...")
letter_sections = re.findall(r'[a-z]{15,}', content_nospace.lower())

print(f"Found {len(letter_sections)} potential sections\n")

decoded_results = []

for i, section in enumerate(letter_sections, 1):
    decoded, nums = decode_hex_section(section)
    
    if decoded.strip():
        print(f"Section {i} ({len(section)} letters):")
        print(f"  Numbers: {nums[:50]}...")
        print(f"  Decoded: {repr(decoded[:100])}")
        
        # Check if it looks like real words
        if any(word in decoded.lower() for word in ['last', 'words', 'pass', 'this', 'matrix', 'command', 'choice', 'four']):
            print(f"  ✓ LIKELY PASSWORD COMPONENT!")
            decoded_results.append(decoded)
        print()

# Save results
if decoded_results:
    output = "\n---\n".join(decoded_results)
    open('hex_decoded.txt', 'w').write(output)
    print("="*70)
    print(f"✓ Saved decoded sections to hex_decoded.txt")
    print("="*70)
else:
    print("✗ No HEX sections decoded")

print("\nNext: Run 04_combine_passwords.py")
