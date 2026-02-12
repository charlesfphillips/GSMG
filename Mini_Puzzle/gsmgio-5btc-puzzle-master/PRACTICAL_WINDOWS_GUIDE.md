# GSMG Puzzle - Practical Windows/WinSCP Solving Guide

## 🎯 Goal
Extract content from Salphaseion HTML, decode it, and decrypt Cosmic Duality to find the private key.

---

## STEP 1: Save the HTML to a File (Using WinSCP)

### What You Have:
The Salphaseion HTML page content (from the document you provided)

### What to Do:

1. **Create a new text file on your Windows computer**
   - Open Notepad
   - Copy the entire HTML document you have
   - Save as: `C:\Users\YourName\Desktop\salphaseion.html`

2. **Use WinSCP to upload it to a Linux server** (if needed)
   - Or work locally on Windows with Python

---

## STEP 2: Extract the Two Main Content Sections

You need to extract two pieces from that HTML:

### Content #1: SALPHASEION (from the textarea)
```
d b b i b f b h c c b e g b i h a b e b e i h b e g g e g e b e b b g e h h e b h h f b a b f d h b e f f c d b b f c c c g b f b e e g g e c b e d c i b f b f f g i g b e e e a b e a b b a b b a b a b b a a a a b a b b b a b a a a b b b a a b a a b b a b a a b a b b b b a a a a b b b a a b b a b b b a b a b a b b a b b a b a b b a b b a a a b b a b a a b a b b b a a b b a b b b a b a a f a e d g g e e d f c b d a b h h g g c a d c f e d d g f d g b g i g a a e d g g i a f a e c g h g g c d a i h e h a h b a h i g c e i f g b f g e f g a i f a b i f a g a e g e a c g b b e a g f g g e e g g a f b a c g f c d b e i f f a a f c i d a h g d e e f g h h c g g a e g d e b h h e g e g h c e g a d f b d i a g e f c i c g g i f d c g a a g g f b i g a i c f b h e c a e c b c e i a i c e b g b g i e c d e g g f g e g a e d g g f i i c i i i f i f h g g c g f g d c d g g e f c b e e i g e f i b g i b g g g h h f b c g i f d e h e d f d a g i c d b h i c g a i e d a e h a h g h h c i h d g h f h b i i c e c b i i c h i h i i i g i d d g e h h d f d c h c b a f g f b h a h e a g e g e c a f e h g c f g g g g c a g f h h g h b a i h i d i e h h f d e g g d g c i h g g g g g h a d a h i g i g b g e c g e d f c d g g a c c d e h i i c i g f b f f h g g a e i d b b e i b b e i i f d g f d h i e e e i e e e c i f d g d a h d i g g f h e g f i a f f i g g b c b c e h c e a b f b e d b i i b f b f d e d e e h g i g f a a i g g a g b e i i c h i e d i f b e h g b c c a h h b i i b i b b i b d c b a h a i d h f a h i i h i c z a g d a f a o a h e i e c g g c h g i c b b h c g b e h c f c o a b i c f d h h c d b b c a g b d a i o b b g b e a d e d d e z c f o b f d h g d o b d g o o i i g d o c d a o o f i d h z s h a b e f o u r f i r s t h i n t i s y o u r l a s t c o m m a n d U 2 F s d G V k X 1 8 6 t Y U 0 h V J B X X U n B U O 7 C 0 + X 4 K U W n W k C v o Z S x b R D 3 w N s G W V H e f v d r d 9 z a b b a a b a b a b b a b b b a a b b b a b a a a b b a a b a b a b b b a a b a Q v X 0 t 8 v 3 j P B 4 o k p s p x e b R i 6 s E 1 B M l 5 H I 8 R k u + K e j U q T v d W O X 6 n Q j S p e p X w G u N / j J s h a b e f a n s t o o
```

### Content #2: COSMIC DUALITY (the encrypted blob)
```
U2FsdGVkX18tP2/gbclQ5tNZuD4shoV3axuUd8J8aycGCAMoYfhZK0JecHTDpTFe
dGJh4SJIP66qRtXvo7PTpvsIjwO8prLiC/sNHthxiGMuqIrKoO224rOisFJZgARi
c7PaJPne4nab8XCFuV3NbfxGX2BUjNkef5hg7nsoadZx08dNyU2b6eiciWiUvu7D
... (thousands of lines) ...
```

### How to Extract with Windows:

**Option A: Manual (if files are small)**
1. Open the HTML in Notepad
2. Find the SALPHASEION textarea content
3. Copy it to a new file: `salphaseion.txt`
4. Repeat for COSMIC DUALITY: `cosmic_duality.txt`

**Option B: Using Python (recommended)**
```python
# Save this as extract.py
import re

html = open('salphaseion.html', 'r').read()

# Extract Salphaseion
salph_match = re.search(r'<h1>\s*SalPhaseIon\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
if salph_match:
    salphaseion = salph_match.group(1).strip()
    open('salphaseion.txt', 'w').write(salphaseion)
    print(f"✓ Extracted Salphaseion ({len(salphaseion)} chars)")

# Extract Cosmic Duality
cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
if cosmic_match:
    cosmic = cosmic_match.group(1).strip()
    open('cosmic_duality.txt', 'w').write(cosmic)
    print(f"✓ Extracted Cosmic Duality ({len(cosmic)} chars)")
```

**Run it:**
```bash
python extract.py
```

---

## STEP 3: Decode ABBA Binary Sections

### What is ABBA?
- **a = 0** (binary digit)
- **b = 1** (binary digit)
- Then convert 8 bits at a time to ASCII characters

### Example:
```
abbab → 01101 (incomplete, need 8 bits)
abbaabab → 01100101 → 101 (decimal) → 'e' (ASCII)
```

### Python Script to Decode:

```python
# Save this as decode_abba.py

def decode_abba(text):
    """Decode ABBA binary: a=0, b=1"""
    # Remove spaces and non-a/b characters
    clean = ''.join(c for c in text.lower() if c in 'ab')
    
    # Convert a→0, b→1
    binary = clean.replace('a', '0').replace('b', '1')
    
    # Decode 8 bits at a time
    result = ""
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        ascii_val = int(byte, 2)
        char = chr(ascii_val)
        result += char
        print(f"Bits {i//8}: {byte} = {ascii_val} = '{char}'")
    
    return result

# Read the salphaseion content
content = open('salphaseion.txt', 'r').read()

# Find all ABBA sections (they look like: abbabbab...)
import re
abba_sections = re.findall(r'(?:a|b){8,}', content)

print(f"\nFound {len(abba_sections)} ABBA sections\n")

for i, section in enumerate(abba_sections, 1):
    print(f"=== ABBA Section {i} ===")
    decoded = decode_abba(section)
    print(f"\nDecoded: {repr(decoded)}")
    print(f"Readable: {decoded}")
    print()
```

**Run it:**
```bash
python decode_abba.py
```

**What you're looking for:** Readable text like "matrixsumlist" or "enter"

---

## STEP 4: Decode Hex Sections (a=1-26, o=0)

### What is This?
- **a=1, b=2, c=3, ... z=26, o=0**
- Convert to decimal numbers
- Interpret as hexadecimal (base-16)
- Convert hex to ASCII

### Example:
```
"agdaf" means:
a=1, g=7, d=4, a=1, f=6
Numbers: 1,7,4,1,6
String: "174161"
As hex pairs: 17 41 61
17₁₆ = 23₁₀ = [control char]
41₁₆ = 65₁₀ = 'A'
61₁₆ = 97₁₀ = 'a'
Result: "Aa"
```

### Python Script:

```python
# Save this as decode_hex.py

def decode_hex_section(text):
    """Decode hex section: a=1-26, o=0"""
    
    # Build the mapping
    char_map = {}
    for i in range(26):
        char_map[chr(ord('a') + i)] = str(i + 1)
    char_map['o'] = '0'
    
    # Convert to number string
    num_str = ''.join(char_map.get(c, '') for c in text.lower() if c in char_map)
    print(f"Number string: {num_str}")
    print(f"Length: {len(num_str)}")
    
    # Method 1: Interpret as hex pairs
    result = ""
    for i in range(0, len(num_str) - 1, 2):
        pair = num_str[i:i+2]
        try:
            val = int(pair, 16)  # Interpret as hexadecimal
            if 32 <= val <= 126:  # Printable ASCII
                result += chr(val)
                print(f"Hex {pair} = {val} = '{chr(val)}'")
            else:
                print(f"Hex {pair} = {val} = [non-printable]")
        except:
            pass
    
    return result

# Read content
content = open('salphaseion.txt', 'r').read()

# Remove spaces
content_nospace = content.replace(' ', '')

# Find hex sections (they look like: agdafaoh...)
import re
hex_sections = re.findall(r'[a-z]+', content_nospace)

# Test each section
for section in hex_sections:
    if len(section) > 20 and any(c in section for c in 'agdaf'):
        print(f"\n=== Testing: {section[:50]}... ===")
        decoded = decode_hex_section(section)
        print(f"\nResult: {decoded}\n")
        
        # Check if looks like real words
        if any(word in decoded.lower() for word in ['last', 'words', 'pass', 'this', 'matrix']):
            print("✓ LIKELY CANDIDATE!")
            open('hex_decoded.txt', 'a').write(f"{decoded}\n")
```

**Run it:**
```bash
python decode_hex.py
```

**What you're looking for:** Text containing "lastwordsbeforearchichoice" or "thispassword"

---

## STEP 5: Combine the Decoded Passwords

### Once you have decoded:
- Section 1: `matrixsumlist`
- Section 2: `enter`
- Section 3: `lastwordsbeforearchichoice`
- Section 4: `thispassword`

### Combine them:

```python
# Save this as create_password.py
import hashlib

# The decoded sections
section1 = "matrixsumlist"
section2 = "enter"
section3 = "lastwordsbeforearchichoice"
section4 = "thispassword"

# Combine (try different combinations)
combinations = [
    section1 + section2 + section3 + section4,
    section1 + section2 + section3,
    section3 + section4,
    section1 + section3,
    section1 + section2 + section4,
]

print("Testing password combinations:\n")

for combo in combinations:
    hash_val = hashlib.sha256(combo.encode()).hexdigest()
    print(f"Password: {combo}")
    print(f"SHA256: {hash_val}\n")
    
    # Save to file for OpenSSL testing
    open('candidates.txt', 'a').write(f"{combo}|{hash_val}\n")

print("Saved to candidates.txt")
```

**Run it:**
```bash
python create_password.py
```

**Output:** List of candidate passwords and their SHA256 hashes

---

## STEP 6: Decrypt with OpenSSL

### You need OpenSSL on Windows

**Option A: Install OpenSSL for Windows**
- Download: https://slproweb.com/products/Win32OpenSSL.html
- Install the full version (not light)
- Add to PATH during installation

**Option B: Use pre-installed (Windows 10+)**
```bash
# Check if you have it
openssl version
```

### Decrypt Command:

```bash
# Method 1: Try with raw password
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:matrixsumlist

# Method 2: Try with hash
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# Method 3: Script to test multiple
for /f "tokens=1,2 delims=|" %%A in (candidates.txt) do (
  echo Testing: %%A
  openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:%%A 2>nul | findstr /c:"private" && (
    echo FOUND! Password is: %%A
    openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:%%A > result.txt
    goto done
  )
)
:done
```

### Windows PowerShell Script (easier):

```powershell
# Save as test_passwords.ps1

$candidates = @(
    "matrixsumlist",
    "enter",
    "lastwordsbeforearchichoice",
    "thispassword",
    "matrixsumlist" + "enter" + "lastwordsbeforearchichoice" + "thispassword"
)

foreach ($pass in $candidates) {
    Write-Host "Testing: $pass" -ForegroundColor Cyan
    
    # Also try with SHA256
    $sha256 = [System.Security.Cryptography.SHA256]::Create()
    $hash = [System.Convert]::ToHexString($sha256.ComputeHash([System.Text.Encoding]::UTF8.GetBytes($pass)))
    
    # Test with OpenSSL
    $result = openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:$hash 2>&1
    
    if ($result -and $result -notmatch "bad decrypt") {
        Write-Host "✓ SUCCESS! Password: $pass" -ForegroundColor Green
        Write-Host "SHA256: $hash" -ForegroundColor Green
        $result | Out-File -FilePath "decrypted.txt"
        break
    }
}
```

**Run it:**
```powershell
powershell -ExecutionPolicy Bypass -File test_passwords.ps1
```

---

## STEP 7: Check Your Result

### If Successful:
- ✓ No "bad decrypt" error
- ✓ You see readable text
- ✓ Contains a Bitcoin private key (long hex string starting with something like "5KJ..." or similar)

### If Not Successful:
- ❌ "bad decrypt" error → wrong password
- ❌ Garbage output → wrong password
- Try different combinations

---

## Complete Workflow (All-in-One)

### Save this as `solve.py`:

```python
#!/usr/bin/env python3
import re
import hashlib
import os

print("="*70)
print("GSMG PUZZLE SOLVER")
print("="*70)

# STEP 1: Extract
print("\n[1] Extracting content from HTML...")
try:
    html = open('salphaseion.html', 'r').read()
    
    salph_match = re.search(r'<h1>\s*SalPhaseIon\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
    cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
    
    salphaseion = salph_match.group(1).strip() if salph_match else ""
    cosmic = cosmic_match.group(1).strip() if cosmic_match else ""
    
    print(f"  ✓ Salphaseion: {len(salphaseion)} chars")
    print(f"  ✓ Cosmic Duality: {len(cosmic)} chars")
    
    open('salphaseion.txt', 'w').write(salphaseion)
    open('cosmic_duality.txt', 'w').write(cosmic)
except Exception as e:
    print(f"  ✗ Error: {e}")
    exit(1)

# STEP 2: Decode ABBA
print("\n[2] Decoding ABBA binary sections...")

def decode_abba(text):
    clean = ''.join(c for c in text.lower() if c in 'ab')
    binary = clean.replace('a', '0').replace('b', '1')
    result = ""
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        ascii_val = int(byte, 2)
        result += chr(ascii_val)
    return result

abba_sections = re.findall(r'(?:a|b){8,}', salphaseion)
abba_results = []

for i, section in enumerate(abba_sections, 1):
    decoded = decode_abba(section)
    if decoded.strip():
        print(f"  Section {i}: {repr(decoded[:50])}")
        abba_results.append(decoded)

# STEP 3: Decode HEX
print("\n[3] Decoding HEX sections (a=1-26, o=0)...")

def decode_hex_section(text):
    char_map = {}
    for i in range(26):
        char_map[chr(ord('a') + i)] = str(i + 1)
    char_map['o'] = '0'
    
    num_str = ''.join(char_map.get(c, '') for c in text.lower() if c in char_map)
    
    result = ""
    for i in range(0, len(num_str) - 1, 2):
        pair = num_str[i:i+2]
        try:
            val = int(pair, 16)
            if 32 <= val <= 126:
                result += chr(val)
        except:
            pass
    return result

content_nospace = salphaseion.replace(' ', '')
hex_sections = re.findall(r'[a-z]{10,}', content_nospace)
hex_results = []

for section in hex_sections:
    decoded = decode_hex_section(section)
    if any(word in decoded.lower() for word in ['last', 'words', 'pass', 'this', 'matrix']):
        print(f"  ✓ Found: {repr(decoded[:50])}")
        hex_results.append(decoded)

# STEP 4: Create candidates
print("\n[4] Creating password candidates...")

all_decoded = abba_results + hex_results
combinations = [
    ''.join(all_decoded),
]

for combo in combinations:
    hash_val = hashlib.sha256(combo.encode()).hexdigest()
    print(f"  Candidate: {combo[:40]}...")
    print(f"  SHA256: {hash_val}")

# STEP 5: Save for OpenSSL testing
print("\n[5] Ready for OpenSSL decryption!")
print(f"\n  File to decrypt: cosmic_duality.txt")
print(f"  Passwords to try: See above")
print(f"\n  Command template:")
print(f"  openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:<PASSWORD_OR_HASH>")

print("\n" + "="*70)
print("Next step: Use OpenSSL to test the passwords above")
print("="*70)
```

**Run it:**
```bash
python solve.py
```

---

## 🎯 Quick Checklist

- [ ] Save HTML to `salphaseion.html`
- [ ] Run extraction script → get `salphaseion.txt` and `cosmic_duality.txt`
- [ ] Run ABBA decoder → get decoded sections
- [ ] Run HEX decoder → get decoded sections
- [ ] Combine decoded sections into password
- [ ] Create SHA256 hash of password
- [ ] Test with OpenSSL
- [ ] Find the private key! 🎉

---

## 💡 Tips

1. **If ABBA decoding produces garbage:** Check if you're reading the section correctly
2. **If HEX decoding doesn't work:** Try different grouping sizes (not just pairs)
3. **If OpenSSL says "bad decrypt":** Wrong password - try the other combinations
4. **If you find the private key:** You've solved it! 🏆

---

Ready to start? Begin with Step 1! Let me know where you get stuck! 🚀
