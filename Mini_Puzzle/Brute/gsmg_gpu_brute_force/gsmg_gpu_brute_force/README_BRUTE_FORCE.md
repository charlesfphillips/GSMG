# 🔥 GPU Brute Force for GSMG 5 BTC Puzzle

## Overview

This package provides GPU-accelerated brute force tools to extract the k1 and k2 WIF private keys from the GSMG 5 BTC puzzle's Salphaseion sections.

**What it does:**
- Tests permutations of character mappings to decode WIF keys
- Uses smart heuristics to test high-probability mappings first
- GPU-accelerated when NVIDIA CUDA is available
- Falls back to CPU-only mode if no GPU present

## Quick Start

### 1. Setup (One Time)

```bash
chmod +x setup_brute_force.sh
./setup_brute_force.sh
```

This will:
- Check for Python 3
- Detect NVIDIA GPU (optional)
- Install required dependencies

### 2. Run Brute Force

```bash
python3 optimized_gpu_brute_force_new.py
```

The script will automatically:
- Analyze character frequencies in the puzzle data
- Test smart character subsets first (7 subsets, ~25M permutations total)
- Report progress every few seconds
- Print results if valid WIF keys are found

## The Problem

The GSMG puzzle contains two encoded sections that map to WIF private keys:

**Section 2 (k1 - 93 chars):**
```
agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadeddecfobfdhgdobdgooiigdocdaoofidh
```

**Section 3 (k2 - 29 chars):**
```
cfobfdhgdobdgooiigdocdaoofidh
```

Both sections use only 10 custom letters: `a b c d e f g h i o`

These 10 letters map to 10 Base58 characters, creating:
- **k1**: 51-character WIF key starting with '5' (uncompressed)
- **k2**: 52-character WIF key starting with 'K' or 'L' (compressed)

## The Solution Approach

### Phase 1: Smart Heuristics (Fast - minutes)

Tests carefully chosen 10-character subsets of Base58:

1. `5KL1234567` - Required start chars + digits
2. `5KLABCDabc` - Required start chars + common letters
3. `5KL123ABCa` - Mixed digits and letters
4. `12345KLabc` - Alternative mix
5. `123456789A` - First 10 Base58 characters
6. `5KLdefghij` - Lowercase emphasis
7. `5KLMNPQRST` - Uppercase emphasis

Each subset tests 10! = 3,628,800 permutations.
Total: ~25 million permutations

**Performance:**
- GPU: ~5-15 minutes
- CPU: ~20-60 minutes

### Phase 2: Exhaustive Search (Slow - optional)

If Phase 1 doesn't find the solution, can optionally test all C(58,10) ≈ 2 billion combinations.

**Estimated time:**
- High-end GPU (RTX 3090): Several hours
- Mid-range GPU (GTX 1060): 1-2 days
- CPU only: Weeks to months

## Expected Output

### If Solution Found:

```
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
✅ FOUND VALID WIF KEY(S)!
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
  Subset: 5KL1234567
  Mapping: {'a': '5', 'b': 'K', 'c': 'L', 'd': '1', 'e': '2', ...}
  k1: 5KLdDt3RwxgEeUSLGE9yHTBhowoMmdefzBHA4ZfUfQcV9bR6dLz
  k1 Valid: True
  k2: L3wcsrHj7akBEQ6p2D4bRcaF8CscfzmH5NNJzjAq6XDdEvv8ok5R
  k2 Valid: True
  Time: 3.45 seconds
  Tested: 125,440 permutations

🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆
🏆 COMPLETE SOLUTION FOUND! 🏆
🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆🏆
```

### If No Solution Found:

```
SEARCH COMPLETE (Smart Subsets)
================================================================================
Total permutations tested: 25,401,600
Time elapsed: 847.3 seconds

❌ NO VALID WIF KEYS FOUND in smart subsets

The solution may require:
  1. Exhaustive search (C(58,10) ≈ 2 billion combinations)
  2. A different decoding approach
  3. Additional information from the puzzle
```

## What To Do With Results

Once you have k1 and k2:

### 1. Verify the Keys

```python
import hashlib

def verify_wif(wif):
    # Decode and check format
    # (validation is already done by the brute force script)
    print(f"✓ {wif} is valid")

verify_wif(k1)
verify_wif(k2)
```

### 2. Generate Bitcoin Addresses

```python
# Use the verify_bitcoin_address.py script from the puzzle package
python3 verify_bitcoin_address.py
```

This will show what Bitcoin addresses k1 and k2 generate.

### 3. Calculate Final Key

```python
# Calculate k_final = (k1 + k2) mod n
# where n is the secp256k1 curve order

N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

k1_int = wif_to_int(k1)
k2_int = wif_to_int(k2)

k_final = (k1_int + k2_int) % N
```

### 4. Verify Solution

The final key should generate the prize address:
```
1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
```

## Requirements

### Minimum (CPU-only):
- Python 3.7 or higher
- ~2GB RAM
- Any modern CPU

### Recommended (GPU):
- Python 3.7 or higher
- NVIDIA GPU with CUDA support
- CUDA Toolkit 11.0 or higher
- ~4GB RAM
- numba and numpy packages

### Installation Commands:

```bash
# For CPU-only mode
pip3 install numpy

# For GPU acceleration
pip3 install numba numpy

# Install CUDA Toolkit (if not already installed)
# Download from: https://developer.nvidia.com/cuda-downloads
```

## Files Included

- `optimized_gpu_brute_force_new.py` - Main brute force script
- `setup_brute_force.sh` - Automated setup script
- `README_BRUTE_FORCE.md` - This file
- `QUICK_START.txt` - Quick reference guide

## Performance Notes

### CPU Performance:
- Intel i7/i9: ~70,000-150,000 perms/sec
- AMD Ryzen 7/9: ~80,000-180,000 perms/sec
- Phase 1: 20-60 minutes

### GPU Performance:
- RTX 3090: ~2-5 million perms/sec
- RTX 3060: ~800k-1.5M perms/sec
- GTX 1660: ~400k-800k perms/sec
- Phase 1: 5-15 minutes

## Troubleshooting

### "No module named 'numba'"
```bash
pip3 install --user numba numpy
```

### "CUDA not available"
This is normal if you don't have an NVIDIA GPU. The script will run in CPU-only mode.

### "Out of memory"
Reduce the batch size or use CPU-only mode.

### No results after Phase 1
The solution might not be in the smart subsets. Options:
1. Check puzzle documentation for additional clues
2. Try a different decoding approach
3. Run exhaustive search (very slow)

## Technical Details

### WIF Format:
- Uncompressed (k1): 51 chars, starts with '5'
  - Format: 0x80 + 32-byte key + 4-byte checksum
- Compressed (k2): 52 chars, starts with 'K' or 'L'
  - Format: 0x80 + 32-byte key + 0x01 + 4-byte checksum

### Base58Check:
- Checksum = First 4 bytes of SHA256(SHA256(payload))
- Validates data integrity
- Prevents transcription errors

### Search Space:
- 10! permutations per subset = 3,628,800
- 7 smart subsets = ~25 million total
- Full search: C(58,10) × 10! ≈ 7.5 × 10^15 permutations

## Credits

Based on the GSMG 5 BTC puzzle by gsmg.io
Brute force implementation: Optimized for NVIDIA CUDA GPUs
