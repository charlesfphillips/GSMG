# GSMG Puzzle Solver

Working on the GSMG.IO 5 BTC puzzle (address: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe).

## Progress
- Decoded phase_cosmic.txt → phase_cosmic.bin (base64)
- Decrypted AES-256-CBC with token XOR chain + EVP_MD5 + blob salt (raw_no_unpad.bin)
- Printable fragments: [:9GR, gxx.<[, $a6x9~, J{J}79, 2; U,', )f 3h\, [t6H`S, etc.
- No direct privkey found — likely hint/checkpoint

## Files
- decoder.py: AES decryption with all variants
- analyzer.py: Salphaseion grid sums/diagonals
- raw_no_unpad.bin: Successful decryption output
- phase_cosmic.bin: Base64-decoded ciphertext

## Next
- Combine grid h1+h2 with clues (1106 multiplier, Dec31 hex XOR, symbols mask, women passphrase, missing g/')
- Test sum variants in grid_final_test.py
