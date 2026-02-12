import hashlib
import binascii

# --- DATA ---
K1_INT = 0x8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af
K2_INT = 0xa986730c9aaeb1b36a12df5962334f9c29a2b6e5e0a6c887b83559063f0d80c2
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# --- MATH ---
P = 2**256 - 2**32 - 977
Gx = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
Gy = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

def scalar_mult(k, point):
    # Pure Python implementation for your environment
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
    
    result = None
    addend = point
    while k:
        if k & 1: result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def get_addr_wif(scalar_int):
    scalar_hex = hex(scalar_int % N)[2:].zfill(64)
    pt = scalar_mult(scalar_int % N, (Gx, Gy))
    # Uncompressed format (matches your previous successful targets)
    pub = '04' + hex(pt[0])[2:].zfill(64) + hex(pt[1])[2:].zfill(64)
    rid = hashlib.new('ripemd160', hashlib.sha256(binascii.unhexlify(pub)).digest()).digest()
    net = b'\x00' + rid
    chk = hashlib.sha256(hashlib.sha256(net).digest()).digest()[:4]
    
    # Base58
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    def b58(data):
        num = int(data.hex(), 16)
        res = ''
        while num > 0:
            num, rem = divmod(num, 58)
            res = alphabet[rem] + res
        return res
    
    addr = b58(net + chk)
    wif_raw = binascii.unhexlify('80' + scalar_hex)
    wif_chk = hashlib.sha256(hashlib.sha256(wif_raw).digest()).digest()[:4]
    wif = b58(wif_raw + wif_chk)
    return addr, wif

# THE "TURING COMPLETE" CALCULATION
# Multiply the components and apply the 12-bit shift
product_int = (K1_INT * K2_INT) % N
shifted_product = ((product_int >> 12) | (product_int << (256 - 12))) & (2**256 - 1)

addr, wif = get_addr_wif(shifted_product)
print(f"Final Treasury Address: 1{addr}") # Ensure leading 1
print(f"Final Treasury WIF:     {wif}")