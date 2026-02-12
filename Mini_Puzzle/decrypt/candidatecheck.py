import hashlib
import binascii

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
K1 = 0x8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af
K2 = 0xa986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2
LUV = 1106

def to_wif(val):
    hex_val = hex(val)[2:].zfill(64)
    raw = binascii.unhexlify('80' + hex_val + '01')
    hash1 = hashlib.sha256(raw).digest()
    hash2 = hashlib.sha256(hash1).digest()
    return binascii.b2a_base64(raw + hash2[:4]).decode().strip() # Simplified for display

# Candidate 1: Midpoint + LUV
mid = ((K1 + K2) * pow(2, -1, N)) % N
c1 = (mid + LUV) % N

# Candidate 2: Midpoint - LUV
c2 = (mid - LUV) % N

# Candidate 3: Midpoint XOR LUV
c3 = mid ^ LUV

print(f"Option 1 (Add): {hex(c1)}")
print(f"Option 2 (Sub): {hex(c2)}")
print(f"Option 3 (XOR): {hex(c3)}")