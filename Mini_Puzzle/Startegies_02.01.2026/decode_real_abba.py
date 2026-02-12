import re

# Read the cleaned Salphaseion content
content = open('/home/claude/salphaseion_real.txt', 'r').read()

print("="*80)
print("DECODING ABBA BINARY SECTIONS FROM REAL FILE")
print("="*80)

# Find all ABBA sections (consecutive a/b characters)
abba_sections = re.findall(r'[ab]{8,}', content)

print(f"\nFound {len(abba_sections)} ABBA sections\n")

decoded_results = []

for i, section in enumerate(abba_sections, 1):
    # Convert a=0, b=1
    binary = section.replace('a', '0').replace('b', '1')
    
    # Decode 8 bits at a time
    decoded = ""
    for j in range(0, len(binary) - 7, 8):
        byte = binary[j:j+8]
        ascii_val = int(byte, 2)
        decoded += chr(ascii_val)
    
    decoded_results.append(decoded)
    print(f"Section {i}:")
    print(f"  Binary length: {len(binary)} bits")
    print(f"  Decoded ({len(decoded)} chars): {repr(decoded)}")
    print()

# Save results
output = "\n".join(decoded_results)
open('/home/claude/abba_decoded_real.txt', 'w').write(output)

print("="*80)
print("✓ Saved decoded ABBA sections to abba_decoded_real.txt")
print("="*80)
print("\nDecodings to test as passwords:")
for i, result in enumerate(decoded_results, 1):
    print(f"  {i}. {result}")

