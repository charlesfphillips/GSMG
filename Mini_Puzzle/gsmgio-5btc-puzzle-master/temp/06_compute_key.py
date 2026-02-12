#!/usr/bin/env python3
import hashlib

print("="*70)
print("STEP 6: COMPUTE AES KEY FROM TOKENS")
print("="*70)

tokens = [
    "matrixsumlist",
    "enter",
    "lastwordsbeforearchichoice",
    "thispassword",
    "matrixsumlist",
    "sha256",
    "theone"
]

hashes = [hashlib.sha256(t.encode()).digest() for t in tokens]  # Use bytes for XOR

xor_key = bytearray(hashes[0])
for h in hashes[1:]:
    for i in range(len(xor_key)):
        xor_key[i] ^= h[i]

key_hex = xor_key.hex()

print(f"Computed AES key (hex): {key_hex}")
print("\nNext: Use in OpenSSL with -K and -iv (see instructions)")
print("="*70)