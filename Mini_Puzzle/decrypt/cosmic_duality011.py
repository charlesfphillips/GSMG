import hashlib
import binascii

def private_key_to_p2sh_segwit_address(priv_hex):
    # 1. Get Public Key (Compressed is required for SegWit)
    # Using the scalar you just generated in duality010
    import bitcoin # Requires 'bitcoin' or 'bit' library
    pk = bitcoin.privkey_to_pubkey(priv_hex)
    
    # 2. Create the P2WPKH Script (0x00 0x14 <hash160>)
    pubkey_bin = binascii.unhexlify(pk)
    sha256_pk = hashlib.sha256(pubkey_bin).digest()
    ripemd160_pk = hashlib.new('ripemd160', sha256_pk).digest()
    redeem_script = b'\x00\x14' + ripemd160_pk
    
    # 3. Hash the Redeem Script (P2SH)
    sha256_rs = hashlib.sha256(redeem_script).digest()
    ripemd160_rs = hashlib.new('ripemd160', sha256_rs).digest()
    
    # 4. Base58Check Encode with Prefix 0x05 (Mainnet P2SH)
    network_rs = b'\x05' + ripemd160_rs
    checksum = hashlib.sha256(hashlib.sha256(network_rs).digest()).digest()[:4]
    
    alphabet = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    num = int((network_rs + checksum).hex(), 16)
    res = ''
    while num > 0:
        num, rem = divmod(num, 58)
        res = alphabet[rem] + res
    return '3' + res

# THE SCALAR FROM YOUR LAST RUN
final_scalar = "29f60ee635ede9078f6b1c4b3cccb357c45d46556ab4ee1934e7c3da30bc67e5"

print(f"P2SH (SegWit) Address: {private_key_to_p2sh_segwit_address(final_scalar)}")