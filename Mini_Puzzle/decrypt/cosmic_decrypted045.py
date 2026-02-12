import hashlib

def base58_encode(hex_str):
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int(hex_str, 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return res

# This is the 'Final WIF Hex' you just generated
final_hex = "80e169d3bf8288d2d09030ea885361d70e64cd27c3e56d0a15d006f4643c8fa88c6b407aa1"
print(f"Final WIF Key: {base58_encode(final_hex)}")