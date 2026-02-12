#!/usr/bin/env python3
"""
GSMG PUZZLE - FINAL SOLUTION
Password: matrixsumlist
Decrypts cosmic_duality_real.txt to get K1 and K2
Tests all transformations to find the one that generates 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
"""

import base64
import hashlib
import binascii
import sys

print("="*80)
print("GSMG PUZZLE - COMPLETE SOLUTION")
print("="*80)

# Step 1: Decrypt cosmic_duality_real.txt
print("\nSTEP 1: Decrypt cosmic_duality_real.txt with password 'matrixsumlist'")
print("-" * 80)

password = b"matrixsumlist"

try:
    with open('cosmic_duality_real.txt', 'r') as f:
        data = f.read()
except:
    print("✗ Could not find cosmic_duality_real.txt")
    print("  Please make sure it's in the current directory")
    sys.exit(1)

# Decode from Base64
data = base64.b64decode(data)

if not data.startswith(b"Salted__"):
    print("✗ Not OpenSSL format")
    sys.exit(1)

salt = data[8:16]
ciphertext = data[16:]

print(f"✓ File loaded and Base64 decoded")
print(f"  Salt: {binascii.hexlify(salt).decode()}")
print(f"  Ciphertext: {len(ciphertext)} bytes")

# EVP_BytesToKey
def evp_bytes_to_key(password_bytes, salt_bytes, key_len=32, iv_len=16):
    d = b""
    while len(d) < key_len + iv_len:
        d = d + hashlib.md5(d + password_bytes + salt_bytes).digest()
    key = d[:key_len]
    iv = d[key_len:key_len + iv_len]
    return key, iv

key, iv = evp_bytes_to_key(password, salt)

# Decrypt
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import unpad
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(plaintext_padded, AES.block_size)
    
    print(f"✓ Decryption successful!")
    print(f"  Plaintext: {len(plaintext)} bytes")
    
    if len(plaintext) != 1343:
        print(f"⚠️  Warning: Expected 1343 bytes, got {len(plaintext)}")
    
except ImportError:
    print("✗ PyCryptodome not installed")
    print("  Install with: pip install pycryptodome")
    sys.exit(1)

# Step 2: Extract K1 and K2
print("\nSTEP 2: Extract K1 and K2 from decrypted data")
print("-" * 80)

K1 = binascii.hexlify(plaintext[0:32]).decode()
K2 = binascii.hexlify(plaintext[671:703]).decode()

print(f"✓ K1: {K1}")
print(f"✓ K2: {K2}")

# Convert to integers
K1_int = int(K1, 16)
K2_int = int(K2, 16)

# secp256k1
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
P = 2**256 - 2**32 - 977
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

# EC point operations
def point_add(p1, p2):
    if p1 is None: return p2
    if p2 is None: return p1
    (x1, y1), (x2, y2) = p1, p2
    if x1 == x2 and y1 != y2: return None
    if x1 == x2:
        m = (3 * x1 * x1) * pow(2 * y1, P - 2, P)
    else:
        m = (y1 - y2) * pow(x1 - x2, P - 2, P)
    x3 = (m * m - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P
    return (x3, y3)

def scalar_mult(k, point):
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def base58_encode(data):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int(data.hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    pad = 0
    for byte in data:
        if byte == 0: pad += 1
        else: break
    return (alphabet[0] * pad) + res

def get_address(scalar_int):
    """Generate Bitcoin address from scalar"""
    try:
        pub_point = scalar_mult(scalar_int, (Gx, Gy))
        if pub_point is None:
            return None, None
        
        x_hex = hex(pub_point[0])[2:].zfill(64)
        y_hex = hex(pub_point[1])[2:].zfill(64)
        
        # Compressed
        pub_hex = '0' + str(2 + (pub_point[1] % 2)) + x_hex
        pub_bin = binascii.unhexlify(pub_hex)
        sha = hashlib.sha256(pub_bin).digest()
        rid = hashlib.new('ripemd160', sha).digest()
        net = b'\x00' + rid
        chk = hashlib.sha256(hashlib.sha256(net).digest()).digest()[:4]
        addr_c = base58_encode(net + chk)
        
        # Uncompressed
        pub_hex = '04' + x_hex + y_hex
        pub_bin = binascii.unhexlify(pub_hex)
        sha = hashlib.sha256(pub_bin).digest()
        rid = hashlib.new('ripemd160', sha).digest()
        net = b'\x00' + rid
        chk = hashlib.sha256(hashlib.sha256(net).digest()).digest()[:4]
        addr_u = base58_encode(net + chk)
        
        return addr_c, addr_u
    except:
        return None, None

# Step 3: Test transformations
print("\nSTEP 3: Test all transformations")
print("-" * 80)

TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

transformations = [
    ("K1 + K2", (K1_int + K2_int) % N),
    ("K2 - K1", (K2_int - K1_int) % N),
    ("K1 - K2", (K1_int - K2_int) % N),
    ("K1 * K2", (K1_int * K2_int) % N),
    ("K1 ^ K2", K1_int ^ K2_int),
    ("K1 << 1", (K1_int << 1) % N),
    ("K2 << 1", (K2_int << 1) % N),
    ("(K1 + K2) ^ K2", ((K1_int + K2_int) % N) ^ K2_int),
]

found = False

for name, scalar in transformations:
    addr_c, addr_u = get_address(scalar)
    
    if addr_c and addr_c == TARGET:
        print(f"\n✓✓✓ FOUND IT! {name}")
        print(f"  Address (compressed): {addr_c}")
        print(f"  Scalar: {hex(scalar)}")
        found = True
        winning_scalar = scalar
        break
    
    if addr_u and addr_u == TARGET:
        print(f"\n✓✓✓ FOUND IT! {name}")
        print(f"  Address (uncompressed): {addr_u}")
        print(f"  Scalar: {hex(scalar)}")
        found = True
        winning_scalar = scalar
        break
    
    if addr_c:
        print(f"  [{name:20}] C: {addr_c[:12]}...")
    if addr_u:
        print(f"  [{name:20}] U: {addr_u[:12]}...")

if not found:
    print(f"\n✗ No transformation produced target address")
    print(f"  This suggests the K1/K2 are still not correct")
else:
    # Step 4: Generate WIF
    print("\nSTEP 4: Generate WIF from winning scalar")
    print("-" * 80)
    
    def int_to_wif(private_key_int, compressed=True):
        """Convert integer to WIF"""
        hex_key = hex(private_key_int)[2:].zfill(64)
        extended_key = bytes.fromhex("80" + hex_key)
        if compressed:
            extended_key += b'\x01'
        
        # Base58check
        checksum = hashlib.sha256(hashlib.sha256(extended_key).digest()).digest()[:4]
        return base58_encode(extended_key + checksum)
    
    wif_compressed = int_to_wif(winning_scalar, compressed=True)
    wif_uncompressed = int_to_wif(winning_scalar, compressed=False)
    
    print(f"✓ WIF (compressed):   {wif_compressed}")
    print(f"✓ WIF (uncompressed): {wif_uncompressed}")
    
    print(f"\n" + "="*80)
    print(f"🎉 SOLUTION FOUND!")
    print(f"="*80)
    print(f"\nTarget Address: {TARGET}")
    print(f"Private Key (hex): {hex(winning_scalar)}")
    print(f"WIF (compressed): {wif_compressed}")
    print(f"\nImport this WIF to Electrum and claim your 2.5 BTC! 🚀")

print("\n")

