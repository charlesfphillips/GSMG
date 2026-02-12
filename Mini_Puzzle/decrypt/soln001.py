import hashlib
import binascii

# --- THE COMPONENTS ---
K1_HEX = "8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af"
K2_HEX = "a986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2"
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# --- MINI EC MATH ENGINE (Pure Python) ---
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
    # Add padding for leading zeros
    pad = 0
    for byte in data:
        if byte == 0: pad += 1
        else: break
    return (alphabet[0] * pad) + res

def generate_full_check(scalar_int, label):
    scalar_hex = hex(scalar_int)[2:].zfill(64)
    print(f"\n=== TESTING: {label} ===")
    
    # 1. Derive Public Key Point
    pub_point = scalar_mult(scalar_int, (Gx, Gy))
    x_hex = hex(pub_point[0])[2:].zfill(64)
    y_hex = hex(pub_point[1])[2:].zfill(64)
    
    formats = [
        ("Compressed", '0' + str(2 + (pub_point[1] % 2)) + x_hex),
        ("Uncompressed", '04' + x_hex + y_hex)
    ]
    
    for fmt_name, pub_hex in formats:
        # Generate Address
        pub_bin = binascii.unhexlify(pub_hex)
        sha = hashlib.sha256(pub_bin).digest()
        rid = hashlib.new('ripemd160', sha).digest()
        net = b'\x00' + rid
        chk = hashlib.sha256(hashlib.sha256(net).digest()).digest()[:4]
        addr = base58_encode(net + chk)
        
        # Generate WIF
        wif_payload = binascii.unhexlify('80' + scalar_hex + ('01' if fmt_name == "Compressed" else ""))
        wif_chk = hashlib.sha256(hashlib.sha256(wif_payload).digest()).digest()[:4]
        wif = base58_encode(wif_payload + wif_chk)
        
        print(f"[{fmt_name}]")
        print(f"  Address: {addr}")
        print(f"  WIF:     {wif}")
        
        if addr.startswith("1G") or addr.startswith("13") or addr.startswith("1P"):
            print("  *** REWARD TARGET DETECTED! ***")
    print("-" * 50)

# --- EXECUTION ---
k1 = int(K1_HEX, 16)
k2 = int(K2_HEX, 16)

generate_full_check((k2 - k1) % N, "K2 - K1 (The Debt)")
generate_full_check((k1 + k2) % N, "K1 + K2 (The Agreement)")
generate_full_check(k1 ^ k2, "K1 XOR K2 (The Duality)")