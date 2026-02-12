#!/bin/bash
# GSMG PUZZLE - COMPLETE SOLUTION
# Decrypts cosmic_duality_real.txt and extracts K1/K2

echo "========================================================================"
echo "GSMG PUZZLE - FINAL SOLUTION"
echo "========================================================================"
echo ""
echo "Step 1: Decrypt cosmic_duality_real.txt"
echo "--------"

# Decrypt the file with password "matrixsumlist"
openssl enc -aes-256-cbc -d -a -in cosmic_duality_real.txt \
    -pass pass:"matrixsumlist" -md sha256 -out cosmic_decrypted.bin

# Check if decryption worked
if [ ! -f cosmic_decrypted.bin ]; then
    echo "✗ Decryption failed!"
    exit 1
fi

SIZE=$(wc -c < cosmic_decrypted.bin)

if [ "$SIZE" -eq 1343 ]; then
    echo "✓ Decryption successful!"
    echo "  File size: $SIZE bytes (PERFECT!)"
else
    echo "✗ Wrong file size: $SIZE bytes (expected 1343)"
    exit 1
fi

echo ""
echo "Step 2: Extract K1 and K2 coordinates"
echo "--------"

python3 << 'PYEOF'
import binascii

with open('cosmic_decrypted.bin', 'rb') as f:
    data = f.read()

# K1 is first 32 bytes
K1 = binascii.hexlify(data[0:32]).decode()
print(f"K1: {K1}")

# K2 is at offset 671-703 (32 bytes)
K2 = binascii.hexlify(data[671:703]).decode()
print(f"K2: {K2}")

# Save to file
with open('k1_k2.txt', 'w') as f:
    f.write(f"Password: matrixsumlist\n")
    f.write(f"File: cosmic_duality_real.txt\n")
    f.write(f"Decrypted size: {len(data)} bytes\n")
    f.write(f"\nK1: {K1}\n")
    f.write(f"K2: {K2}\n")

print(f"\n✓ Saved to k1_k2.txt")
PYEOF

echo ""
echo "Step 3: Test transformations to find the right formula"
echo "--------"

python3 << 'PYEOF'
import binascii
import hashlib

# Read K1 and K2
with open('k1_k2.txt', 'r') as f:
    lines = f.readlines()

K1_HEX = lines[4].strip().split(': ')[1]
K2_HEX = lines[5].strip().split(': ')[1]

K1 = int(K1_HEX, 16)
K2 = int(K2_HEX, 16)

# secp256k1 curve order
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
P = 2**256 - 2**32 - 977
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

# Point addition
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
    try:
        pub_point = scalar_mult(scalar_int, (Gx, Gy))
        if pub_point is None:
            return None
        
        x_hex = hex(pub_point[0])[2:].zfill(64)
        y_hex = hex(pub_point[1])[2:].zfill(64)
        
        # Compressed
        pub_hex = '0' + str(2 + (pub_point[1] % 2)) + x_hex
        pub_bin = binascii.unhexlify(pub_hex)
        sha = hashlib.sha256(pub_bin).digest()
        rid = hashlib.new('ripemd160', sha).digest()
        net = b'\x00' + rid
        chk = hashlib.sha256(hashlib.sha256(net).digest()).digest()[:4]
        return base58_encode(net + chk)
    except:
        return None

TARGET = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

transformations = [
    ("K1 + K2", (K1 + K2) % N),
    ("K2 - K1", (K2 - K1) % N),
    ("K1 - K2", (K1 - K2) % N),
    ("K1 * K2", (K1 * K2) % N),
    ("K1 ^ K2", K1 ^ K2),
]

print(f"Testing transformations...")
print(f"Target: {TARGET}\n")

for name, scalar in transformations:
    addr = get_address(scalar)
    if addr == TARGET:
        print(f"✓✓✓ FOUND IT: {name}")
        print(f"  Address: {addr}")
        print(f"  Scalar: {hex(scalar)}")
        
        # Save winner
        with open('winning_scalar.txt', 'w') as f:
            f.write(f"Winning transformation: {name}\n")
            f.write(f"Scalar: {hex(scalar)}\n")
            f.write(f"Address: {addr}\n")
        break
    else:
        if addr:
            print(f"  [{name:10}] {addr}")

PYEOF

echo ""
echo "========================================================================"
echo "✓ Solution complete! Check k1_k2.txt and winning_scalar.txt"
echo "========================================================================"
