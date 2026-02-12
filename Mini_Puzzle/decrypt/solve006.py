import base64
import binascii

# What did your decrypt actually produce?
with open('cosmic_decrypted.bin', 'rb') as f:
    data = f.read()

print(f"Total bytes: {len(data)}")
print(f"First 32 bytes (K1): {binascii.hexlify(data[:32]).decode()}")
print(f"Bytes 671-702 (K2): {binascii.hexlify(data[671:703]).decode()}")