import hashlib
import base58

# Correct mapping: a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=8, i=9, o=0
mapping = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','o':'0'}

# The raw puzzle strings
S2 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"
S3 = "cfobfdhgdobdgooiigdocdaoofidh"

# 1. Convert strings to large integers
n1 = int("".join(mapping[c] for c in S2))
n2 = int("".join(mapping[c] for c in S3))

# 2. Perform the Matrix Sum (Addition)
final_int = n1 + n2

# 3. Convert sum to 32-byte Hex Private Key
# We use the modular order of the curve (N) to ensure it's a valid key
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
final_priv_hex = hex(final_int % N)[2:].zfill(64)

# 4. Generate the final WIF
def to_wif(hex_key):
    extended = b'\x80' + bytes.fromhex(hex_key) + b'\x01' # Compressed
    h = hashlib.sha256(hashlib.sha256(extended).digest()).digest()
    return base58.b58encode(extended + h[:4]).decode()

print(f"--- FINAL PRIZE ATTEMPT ---")
print(f"Hex Key: {final_priv_hex}")
print(f"WIF Key: {to_wif(final_priv_hex)}")