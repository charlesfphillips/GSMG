import hashlib
import base58

def wif_to_int(wif):
    """Converts a WIF string to a raw integer."""
    decoded = base58.b58decode_check(wif)
    raw_key = decoded[1:]
    if len(raw_key) == 33 and raw_key[-1] == 1:
        raw_key = raw_key[:-1]
    return int(raw_key.hex(), 16)

def int_to_wif(private_key_int, compressed=True):
    """Converts a raw integer back to a WIF string."""
    hex_key = hex(private_key_int)[2:].zfill(64)
    extended_key = bytes.fromhex("80" + hex_key)
    if compressed:
        extended_key += b'\x01'
    return base58.b58encode_check(extended_key).decode('utf-8')

k1_wif = "5KLdDt3RwxgEeUSLGE9yHTBhowoMmdefzBHA4ZfUfQcV9bR6dLz"  # Your Uncompressed key
k2_wif = "L3wcsrHj7akBEQ6p2D4bRcaF8CscfzmH5NNJzjAq6XDdEvv8ok5R"  # Your Compressed key

# secp256k1 Curve Order
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

val1 = wif_to_int(k1_wif)
val2 = wif_to_int(k2_wif)

# Calculation: (k1 + k2) mod n
final_priv_int = (val1 + val2) % N
final_wif = int_to_wif(final_priv_int, compressed=True)

print(f"Target Private Key (WIF): {final_wif}")