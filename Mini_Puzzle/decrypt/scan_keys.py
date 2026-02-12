with open('cosmic_decrypted.bin', 'rb') as f:
    data = f.read()
for i in range(0, len(data)-32, 1):  # slide window
    block = data[i:i+32]
    if all(0x20 <= b <= 0x7e for b in block):  # printable
        print(f"Offset {i}: {block.hex()}")
    elif len(block) == 32 and block[0] in (0x02, 0x03, 0x04):  # possible compressed/uncompressed pubkey
        print(f"Pubkey candidate at {i}: {block.hex()}")