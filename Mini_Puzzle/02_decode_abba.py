#!/usr/bin/env python3
"""
STEP 2: Decode ABBA Binary Sections (a=0, b=1)
"""
import re

print("="*70)
print("STEP 2: DECODE ABBA BINARY SECTIONS")
print("="*70)

def decode_abba(text):
    """Decode ABBA: a=0, b=1 -> binary -> ASCII"""
    clean = ''.join(c for c in text.lower() if c in 'ab')
    binary = clean.replace('a', '0').replace('b', '1')
    
    result = ""
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        try:
            ascii_val = int(byte, 2)
            result += chr(ascii_val)
        except:
            pass
    return result

try:
    content = open('salphaseion_content.txt', 'r').read()
    print("\n✓ Opened salphaseion_content.txt")
except FileNotFoundError:
    print("\n✗ ERROR: salphaseion_content.txt not found!")
    print("  Please run 01_extract.py first")
    exit(1)

# Find all ABBA sections (consecutive a/b characters)
print("\nSearching for ABBA binary sections...")
abba_sections = re.findall(r'[ab]{8,}', content.lower())

print(f"Found {len(abba_sections)} ABBA sections\n")

decoded_results = []

for i, section in enumerate(abba_sections, 1):
    decoded = decode_abba(section)
    
    if decoded.strip():
        decoded_results.append(decoded)
        print(f"Section {i} ({len(section)} bits):")
        print(f"  Decoded ({len(decoded)} chars): {repr(decoded[:100])}")
        print()

# Save results
if decoded_results:
    output = "\n".join(decoded_results)
    open('abba_decoded.txt', 'w').write(output)
    print("="*70)
    print(f"✓ Saved {len(decoded_results)} decoded sections to abba_decoded.txt")
    print("="*70)
    print("\nLooking for PASSWORD HINTS in decoded sections:")
    for decoded in decoded_results:
        if any(word in decoded.lower() for word in ['matrix', 'enter', 'list', 'pass', 'key']):
            print(f"  ✓ FOUND: {decoded[:100]}")
else:
    print("✗ No ABBA sections found or decoded")

print("\nNext: Run 03_decode_hex.py")
