import hashlib
import binascii

# --- DATA FROM PREVIOUS SUCCESSFUL RUN ---
K1_INT = 0x8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af
K2_INT = 0xa986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# --- MATH ENGINE ---
P = 2**256 - 2**32 - 977
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

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

def ror12(val):
    """Circular Right Shift by 12 bits for a 256-bit integer."""
    return ((val >> 12) | (val << (256 - 12))) & (2**256 - 1)

def run_transcendence(scalar_int, label):
    # Apply the Women (12) Shift
    shifted_int = ror12(scalar_int) % N
    scalar_hex = hex(shifted_int)[2:].zfill(64)
    
    print(f"\n--- TRANSCENDED: {label} ---")
    pub_point = scalar_mult(shifted_int, (Gx, Gy))
    x_hex = hex(pub_point[0])[2:].zfill(64)
    y_hex = hex(pub_point[1])[2:].zfill(64)
    
    # We focus on Uncompressed as it matched the 1Gy/1P signatures
    pub_hex = '04' + x_hex + y_hex
    pub_bin = binascii.unhexlify(pub_hex)
    rid = hashlib.new('ripemd160', hashlib.sha256(pub_bin).digest()).digest()
    net = b'\x00' + rid
    addr = base58_encode(net + hashlib.sha256(hashlib.sha256(net).digest()).digest()[:4])
    
    wif_payload = binascii.unhexlify('80' + scalar_hex)
    wif = base58_encode(wif_payload + hashlib.sha256(hashlib.sha256(wif_payload).digest()).digest()[:4])
    
    print(f"  Address: {addr}")
    print(f"  WIF:     {wif}")
    if addr.startswith("1G") or addr.startswith("13") or addr.startswith("1P"):
        print("  *** TRANSCENDED REWARD TARGET DETECTED! ***")

# --- EXECUTION ---
run_transcendence((K1_INT + K2_INT) % N, "Shifted Agreement")
run_transcendence(K1_INT ^ K2_INT, "Shifted Duality")