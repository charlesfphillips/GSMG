import hashlib
import binascii

TARGET_ADDR = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"

# Your extracted chunks
chunks = [
    "d353548d1007c81ad1f1601a6c46677c96ccaf0d2a4067e65d0355b1fb07ddf8",
    "3fbc051338ac928bf2e7fc0a9c9b67182b2a1f15377565c6e913736a9b19c018",
    "b68de6b85459c570b1bdfe159f9078ba910303178c668a76de272d5b6cc5814c",
    "ce9b76eece692f2d84c5a4ab51d4902c69260e89ba626ce7a2b26bc873319f7d"
]

def b58encode(v):
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    n = int.from_bytes(v, 'big')
    res = []
    while n > 0:
        n, r = divmod(n, 58)
        res.append(alphabet[r])
    pad = 0
    for b in v:
        if b == 0: pad += 1
        else: break
    return "1" * pad + "".join(res[::-1])

def hex_to_wif(hex_str, compressed=True):
    prefix = "80" + hex_str + ("01" if compressed else "")
    data = binascii.unhexlify(prefix)
    checksum = hashlib.sha256(hashlib.sha256(data).digest()).digest()[:4]
    return b58encode(data + checksum)

print(f"Searching for private key to: {TARGET_ADDR}\n")

for i, h in enumerate(chunks, 2):
    wif_c = hex_to_wif(h, True)
    wif_u = hex_to_wif(h, False)
    print(f"CHUNK {i}:")
    print(f"  WIF (Comp):   {wif_c}")
    print(f"  WIF (Uncomp): {wif_u}")
    
    # Note: To verify the address itself, you'd need the SECP256K1 math.
    # For now, generate the WIFs and check them in Electrum's 'Sweep' tool.