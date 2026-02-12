# Try skipping first N bytes (common for custom headers)
for offset in [0, 4, 8, 16, 32]:
    with open('cosmic_decrypted.bin', 'rb') as f:
        f.seek(offset)
        try:
            decom = zlib.decompress(f.read(), -zlib.MAX_WBITS)
            print(f"Success at offset {offset}: {len(decom)} bytes")
            with open(f'decomp_offset_{offset}.bin', 'wb') as out:
                out.write(decom)
        except:
            pass