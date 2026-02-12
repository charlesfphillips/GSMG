#!/usr/bin/env python3
"""
STEP 4: Combine Decoded Passwords and Create Candidates
"""
import hashlib
import os

print("="*70)
print("STEP 4: CREATE PASSWORD CANDIDATES")
print("="*70)

# Read decoded sections
decoded_sections = []

if os.path.exists('abba_decoded.txt'):
    with open('abba_decoded.txt', 'r') as f:
        decoded_sections.extend(f.read().strip().split('\n'))
    print(f"\n✓ Loaded {len(decoded_sections)} ABBA decoded sections")

if os.path.exists('hex_decoded.txt'):
    with open('hex_decoded.txt', 'r') as f:
        hex_content = f.read().strip().split('---')
        decoded_sections.extend([x.strip() for x in hex_content if x.strip()])
    print(f"✓ Loaded HEX decoded sections")

print(f"\nTotal sections: {len(decoded_sections)}")
print("\nSections loaded:")
for i, section in enumerate(decoded_sections, 1):
    print(f"  {i}. {section[:50]}...")

# Create combinations
print("\n" + "="*70)
print("CREATING PASSWORD CANDIDATES...")
print("="*70)

combinations = [
    ''.join(decoded_sections),  # All combined
]

# Add partial combinations
if len(decoded_sections) >= 2:
    combinations.append(''.join(decoded_sections[:2]))
if len(decoded_sections) >= 3:
    combinations.append(''.join(decoded_sections[1:3]))

candidates = []

for combo in combinations:
    if not combo.strip():
        continue
    
    # Try both raw and hashed
    candidates.append((combo, "raw"))
    
    hash_val = hashlib.sha256(combo.encode()).hexdigest()
    candidates.append((combo, hash_val))

# Display candidates
print(f"\nPassword Candidates ({len(candidates)} total):\n")

for i, (password, variant) in enumerate(candidates, 1):
    if variant == "raw":
        print(f"{i}. Raw password:")
        print(f"   {password[:100]}")
    else:
        print(f"{i}. SHA256 hash:")
        print(f"   {variant}")
    print()

# Save to file for OpenSSL testing
with open('test_passwords.txt', 'w') as f:
    for password, variant in candidates:
        if variant == "raw":
            f.write(f"RAW|{password}\n")
        else:
            f.write(f"SHA256|{variant}\n")

print("="*70)
print("✓ Saved to test_passwords.txt")
print("="*70)
print("\nNext: Use OpenSSL to test these passwords:")
print("  openssl enc -aes-256-cbc -d -a -in cosmic_duality_content.txt -pass pass:<PASSWORD>")
