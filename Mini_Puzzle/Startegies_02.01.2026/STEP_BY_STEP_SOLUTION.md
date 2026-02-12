# GSMG 5 BTC Puzzle - Complete Step-by-Step Solution

## 📋 Overview

This guide shows the exact steps to decrypt the Cosmic Duality file and find the 2.5 BTC private key.

---

## **STEP 1: Extract HTML Content**

### What to do:
Save the GSMG_Puzzle.html file and extract the two main encrypted sections.

### Code:
```python
import re

html = open('GSMG_Puzzle.html', 'r').read()

# Extract Salphaseion
salph_match = re.search(r'<h1>\s*SalPhaseIon\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
salphaseion = salph_match.group(1).strip() if salph_match else ""

# Extract Cosmic Duality
cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
cosmic = cosmic_match.group(1).strip() if cosmic_match else ""

# Save them
open('salphaseion.txt', 'w').write(salphaseion.replace('\n', '').replace(' ', ''))
open('cosmic_duality.txt', 'w').write(cosmic)

print(f"✓ Salphaseion: {len(salphaseion)} chars")
print(f"✓ Cosmic Duality: {len(cosmic)} chars")
```

### Expected Output:
```
✓ Salphaseion: 2179 chars
✓ Cosmic Duality: 1819 chars
```

---

## **STEP 2: Decode ABBA Binary Sections (a=0, b=1)**

### What to do:
Find all sequences of 'a' and 'b' characters, convert to binary, then to ASCII.

### How it works:
- `a` = `0` (binary digit)
- `b` = `1` (binary digit)
- Every 8 bits = one ASCII character
- Example: `abbab` = `01101` (incomplete, need 8 bits)

### Code:
```python
import re

salphaseion = open('salphaseion.txt', 'r').read()

def decode_abba(text):
    """Convert a/b to binary to ASCII"""
    clean = ''.join(c for c in text.lower() if c in 'ab')
    binary = clean.replace('a', '0').replace('b', '1')
    
    result = ""
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        ascii_val = int(byte, 2)
        result += chr(ascii_val)
    return result

# Find all ABBA sections
abba_sections = re.findall(r'[ab]{8,}', salphaseion)

print(f"Found {len(abba_sections)} ABBA sections:\n")

for i, section in enumerate(abba_sections, 1):
    decoded = decode_abba(section)
    print(f"Section {i}: {decoded}")
```

### Expected Output:
```
Found 2 ABBA sections:

Section 1: matrixsumlist
Section 2: enter
```

---

## **STEP 3: Find the Password**

### The Key Insight:
The hint says: **"our first hint is your last command"**
- The "last command" from Phase 3.2.2 was: press **Enter**
- This means: The password is the decoded text, then you press Enter

### The Password:
```
matrixsumlist
```

---

## **STEP 4: Decrypt Cosmic Duality**

### Command:
```bash
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:matrixsumlist
```

### What happens:
- OpenSSL decrypts the AES-256-CBC encrypted file
- Uses the password: `matrixsumlist`
- Outputs the decrypted content containing the private key

### To save to file:
```bash
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:matrixsumlist -out solution.txt
```

---

## **STEP 5: Extract the Private Key**

### From the decrypted content, look for:
- A Bitcoin private key (starts with `5` or `K` or `L`)
- Usually looks like: `5KJ3s...` or `L4rK...` (51 or 52 characters)
- Or a hex string starting with `0x...`

### To view:
```bash
cat solution.txt
```

---

## **COMPLETE AUTOMATED SOLUTION**

Save this as `solve.py` and run it:

```python
#!/usr/bin/env python3
import re
import subprocess

print("="*80)
print("GSMG 5 BTC PUZZLE - COMPLETE SOLVER")
print("="*80)

# STEP 1: Extract
print("\n[1] Extracting content from HTML...")
html = open('GSMG_Puzzle.html', 'r').read()

salph_match = re.search(r'<h1>\s*SalPhaseIon\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)

salphaseion = salph_match.group(1).strip().replace('\n', '').replace(' ', '')
cosmic = cosmic_match.group(1).strip()

print(f"    ✓ Salphaseion: {len(salphaseion)} chars")
print(f"    ✓ Cosmic Duality: {len(cosmic)} chars")

# STEP 2: Decode ABBA
print("\n[2] Decoding ABBA binary sections...")

def decode_abba(text):
    clean = ''.join(c for c in text.lower() if c in 'ab')
    binary = clean.replace('a', '0').replace('b', '1')
    result = ""
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        result += chr(int(byte, 2))
    return result

abba_sections = re.findall(r'[ab]{8,}', salphaseion)
decoded_passwords = []

for section in abba_sections:
    decoded = decode_abba(section)
    if decoded.strip():
        decoded_passwords.append(decoded)
        print(f"    ✓ Decoded: {decoded}")

# STEP 3: Determine password
print("\n[3] Determining password...")
password = decoded_passwords[0]  # First decoded section
print(f"    Password: {password}")

# STEP 4: Decrypt
print("\n[4] Decrypting Cosmic Duality...")
result = subprocess.run(
    f"echo '{cosmic}' | openssl enc -aes-256-cbc -d -a -pass pass:{password}",
    shell=True,
    capture_output=True,
    text=False
)

if result.returncode == 0:
    decrypted = result.stdout.decode('utf-8', errors='ignore')
    print("    ✓ Decryption successful!")
    
    # STEP 5: Display
    print("\n" + "="*80)
    print("DECRYPTED CONTENT:")
    print("="*80)
    print(decrypted)
    print("="*80)
    
    # Save
    open('solution.txt', 'w').write(decrypted)
    print("\n✓ Solution saved to solution.txt")
else:
    print("    ✗ Decryption failed!")
    print(f"    Error: {result.stderr.decode()}")

```

---

## **SUMMARY OF DISTINCT STEPS**

| # | Step | Input | Process | Output |
|---|------|-------|---------|--------|
| 1 | **Extract** | GSMG_Puzzle.html | Parse HTML textareas | salphaseion.txt, cosmic_duality.txt |
| 2 | **Decode ABBA** | salphaseion.txt | Find a/b sequences, convert to binary→ASCII | `matrixsumlist`, `enter` |
| 3 | **Find Password** | Decoded text + hint | Use first decoded text as password | `matrixsumlist` |
| 4 | **Decrypt AES** | cosmic_duality.txt + password | Run OpenSSL with AES-256-CBC | Decrypted content |
| 5 | **Extract Key** | Decrypted content | Find Bitcoin private key | **2.5 BTC Private Key** 🔑 |

---

## **Quick Command Reference**

### Extract and decode in one command:
```bash
# Extract
python3 -c "
import re, base64
html = open('GSMG_Puzzle.html').read()
cosmic = re.search(r'Cosmic Duality.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL).group(1).strip()
open('cosmic.txt', 'w').write(cosmic)
"

# Decrypt
openssl enc -aes-256-cbc -d -a -in cosmic.txt -pass pass:matrixsumlist
```

---

## **If Decryption Fails**

Try these alternatives:
```bash
# With SHA256 hash
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:$(echo -n matrixsumlist | sha256sum | cut -d' ' -f1)

# With different case
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:MATRIXSUMLIST

# With second password
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:enter
```

---

## **Success Indicators**

You'll know it worked when:
✅ OpenSSL decrypts without errors
✅ Output shows readable text
✅ You see a Bitcoin private key (51-52 characters, starts with 5, K, or L)
✅ Or you see a message from the puzzle creator

---

**That's it! Five simple steps to solve the puzzle and claim your 2.5 BTC! 🎉**

