import hashlib

def int_to_wif(n, compressed=False):
    # Convert integer to 32 bytes
    key_bytes = n.to_bytes(32, 'big')
    # Add version byte 0x80
    extended = b'\x80' + key_bytes
    if compressed: extended += b'\x01'
    # Double SHA-256 Checksum
    checksum = hashlib.sha256(hashlib.sha256(extended).digest()).digest()[:4]
    # Simple Base58 encoding would go here...
    return (extended + checksum).hex() # Let's just look at the hex for now

# Testing Section 3 (the shorter one)
S3 = "cfobfdhgdobdgooiigdocdaoofidh"
mapping = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','o':'0'}
s3_digits = "".join(mapping[char] for char in S3)
n2 = int(s3_digits)

print(f"Integer Value: {n2}")
print(f"Hex Private Key: {hex(n2)}")