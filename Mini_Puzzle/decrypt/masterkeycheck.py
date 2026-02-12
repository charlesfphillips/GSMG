import hashlib
import binascii

def openssl_kdf_check(passphrase_bytes, salt_bytes):
    d1 = hashlib.md5(passphrase_bytes + salt_bytes).digest()
    d2 = hashlib.md5(d1 + passphrase_bytes + salt_bytes).digest()
    d3 = hashlib.md5(d2 + passphrase_bytes + salt_bytes).digest()
    return (d1 + d2 + d3)[32:48].hex()

# DATA
MASTER_HEX = "818af53daa3028449f125a2e4f47259ddf9b9d86e59ce6c4993a67ffd76bb402"
MASK_HEX   = "844e86a69a04eea672049e0e0e8612" # From your earlier notes
SALT_BYTES = binascii.unhexlify("2d3f6fe06dc950e6")
TARGET_IV  = "c6ff2e39d98843bc3c26b8a33a15b5c9"

def xor_mask(h1, m1):
    b1 = binascii.unhexlify(h1)
    bm = binascii.unhexlify(m1)
    # Loop mask if shorter
    bm_looped = (bm * (len(b1) // len(bm) + 1))[:len(b1)]
    return bytes(a ^ b for a, b in zip(b1, bm_looped))

# Test 1: XORed Master Key
xor_pass = xor_mask(MASTER_HEX, MASK_HEX)
# Test 2: Literal "theone" (from your tokens)
# Test 3: The Phase 5 Key itself (already likely failed in your run)

print(f"Testing XORed Master Key...")
derived = openssl_kdf_check(xor_pass, SALT_BYTES)
print(f"Derived: {derived}")
print(f"Target:  {TARGET_IV}")

if derived == TARGET_IV:
    print("✅ SUCCESS: The XORed Master Key is the Passphrase!")