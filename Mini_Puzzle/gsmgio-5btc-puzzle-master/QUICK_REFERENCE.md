# GSMG Puzzle - Quick Reference Card

## 🔐 All Known Passwords & Hashes

### Phase Passwords (Documented)
```
Phase 2 Hidden Form Password:
  theflowerblossomsthroughwhatseemstobeaconcretesurface

Phase 3 AES Password:
  causality
  
Phase 3 AES Password (SHA256):
  eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf

Phase 3.1 Concatenated String:
  causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1

Phase 3.1 SHA256:
  1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5

Phase 3.2 AES Password:
  jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple

Phase 3.2 AES Password (SHA256):
  250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c

Phase 3.2.1 Beaufort Cipher Key:
  THEMATRIXHASYOU

Phase 3.2.2 VIC Cipher Alphabet:
  FUBCDORA.LETHINGKYMVPS.JQZXW
  
Phase 3.2.2 VIC Cipher Digits:
  digit 1 = 1
  digit 2 = 4
```

---

## 🎯 Salphaseion Decoded Sections (Expected)

### ABBA Binary Section #1
```
Input type: a=0, b=1 (binary)
Expected output: matrixsumlist
```

### ABBA Binary Section #2
```
Input type: a=0, b=1 (binary)
Expected output: enter
```

### Hex Section #1 (a=1-26, o=0)
```
Input type: a=1, b=2, ..., z=26, o=0 (then convert to hex)
Expected output: lastwordsbeforearchichoice
```

### Hex Section #2 (a=1-26, o=0)
```
Input type: a=1, b=2, ..., z=26, o=0 (then convert to hex)
Expected output: thispassword
```

### Text Hint
```
"shabef our first hint is your last command"
= "sha256" + "our first hint is your last command"
Meaning: Use SHA256 hash; first phase hint needed for final password
```

---

## 🔑 Cosmic Duality Password Candidates (To Try)

### Candidate #1 (Most Likely)
```bash
# Combine Salphaseion decoded sections and hash
password="matrixsumlist" + "enter" + "lastwordsbeforearchichoice" + "thispassword"
hash=$(echo -n "$password" | sha256sum | cut -d' ' -f1)

openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:$hash
```

### Candidate #2
```bash
# Use existing Phase 3.1 hash
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt \
  -pass pass:1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
```

### Candidate #3
```bash
# Use existing Phase 3.2 hash
openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt \
  -pass pass:250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c
```

### Candidate #4
```bash
# Try each decoded section individually
for pass in "matrixsumlist" "enter" "lastwordsbeforearchichoice" "thispassword"; do
  openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:"$pass" 2>/dev/null | head -5
done
```

### Candidate #5
```bash
# Try with hashes of individual sections
for pass in "matrixsumlist" "enter" "lastwordsbeforearchichoice" "thispassword"; do
  hash=$(echo -n "$pass" | sha256sum | cut -d' ' -f1)
  openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:"$hash" 2>/dev/null | head -5
done
```

### Candidate #6
```bash
# Try concatenation with hyphens/underscores
for sep in "" "-" "_" ","; do
  pass="matrixsumlist${sep}enter${sep}lastwordsbeforearchichoice${sep}thispassword"
  hash=$(echo -n "$pass" | sha256sum | cut -d' ' -f1)
  openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:"$hash" 2>/dev/null | head -5
done
```

---

## 📊 Encoding Reference

### ABBA Binary (a=0, b=1)
```
Example: abbab = 01101
ASCII conversion: 01101000 = 'h'

Decode process:
1. Extract only 'a' and 'b' characters
2. Replace: a→0, b→1
3. Group into 8-bit chunks
4. Convert each chunk to ASCII character
```

### Hex Encoding (a=1-26, o=0)
```
Example: "agdaf" with mapping a=1, g=7, d=4, a=1, f=6
Numeric: 1-7-4-1-6
As hex pairs: "17" "41" "6?" (incomplete)
17₁₆ = 23₁₀ = [non-printable]
41₁₆ = 65₁₀ = 'A'
6?₁₆ = needs next digit

Decode process:
1. Map each letter: a=1, b=2, ..., z=26, o=0
2. Concatenate into long number string
3. Group into pairs
4. Interpret each pair as hex (base-16)
5. Convert to ASCII
```

### AES-256-CBC Decryption
```bash
# General format
openssl enc -aes-256-cbc -d -a -in <inputfile> -pass pass:<password>

Flags:
  -aes-256-cbc    = cipher type
  -d              = decrypt (vs -e for encrypt)
  -a              = base64 encoded input
  -in <file>      = input file
  -pass pass:X    = password (can also use file:X or stdin)

Common issues:
  "bad decrypt"   = wrong password
  "no start line"  = not base64 encoded
  "Segmentation fault" = corrupted data
```

---

## 🛠️ Tools & Commands Quick Copy

### Extract Salphaseion Sections
```python
import re

html = open('salphaseion.html').read()

# Find Salphaseion content
salph_match = re.search(r'<h1>\s*SalPhaseIon\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
salphaseion = salph_match.group(1).strip() if salph_match else ""

# Find Cosmic Duality content
cosmic_match = re.search(r'<h1>\s*Cosmic Duality\s*</h1>.*?<textarea[^>]*>(.+?)</textarea>', html, re.DOTALL)
cosmic = cosmic_match.group(1).strip() if cosmic_match else ""

# Save to files
open('salphaseion.txt', 'w').write(salphaseion)
open('cosmic_duality.txt', 'w').write(cosmic)
```

### Decode ABBA Section
```python
def decode_abba(text):
    clean = ''.join(c for c in text if c in 'ab')
    binary = clean.replace('a', '0').replace('b', '1')
    result = ""
    for i in range(0, len(binary)-7, 8):
        result += chr(int(binary[i:i+8], 2))
    return result
```

### Decode Hex Section (a=1-26, o=0)
```python
def decode_hex_section(text):
    char_map = {chr(ord('a')+i): str(i+1) for i in range(26)}
    char_map['o'] = '0'
    nums = ''.join(char_map.get(c, '') for c in text)
    
    result = ""
    for i in range(0, len(nums)-1, 2):
        pair = nums[i:i+2]
        try:
            val = int(pair, 16)
            if 32 <= val <= 126:
                result += chr(val)
        except:
            pass
    return result
```

### Hash a String
```bash
echo -n "your_text_here" | sha256sum | cut -d' ' -f1
```

### Test Multiple Passwords
```bash
#!/bin/bash
passwords=(
  "matrixsumlist"
  "enter"
  "lastwordsbeforearchichoice"
  "thispassword"
  "1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5"
  "250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c"
)

for pass in "${passwords[@]}"; do
  echo "Testing: $pass"
  result=$(openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:"$pass" 2>/dev/null | head -1)
  if [ ! -z "$result" ]; then
    echo "  ✓ SUCCESS!"
    openssl enc -aes-256-cbc -d -a -in cosmic_duality.txt -pass pass:"$pass"
    break
  else
    echo "  ✗ Failed"
  fi
done
```

---

## 📍 Important URLs

```
Main Puzzle: https://gsmg.io/puzzle
Phase 2: https://gsmg.io/theseedisplanted
Salphaseion: https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32

Online Tools:
- Substitution Cipher: https://www.dcode.fr/substitution-cipher
- Base-26: https://www.dcode.fr/base-26-cipher
- Beaufort: https://ciphertools.co.uk/decode.php
- VIC Cipher: https://www.dcode.fr/vic-cipher
- SHA256: https://xorbin.com/tools/sha256-hash-calculator
```

---

## ✅ Success Checklist

- [ ] Extract Salphaseion HTML content
- [ ] Parse into sections (separated by ' z ')
- [ ] Decode first ABBA section → should get text
- [ ] Decode second ABBA section → should get text
- [ ] Decode hex section → should contain "lastwords" or "password"
- [ ] Identify text hints → "shabef our first hint is your last command"
- [ ] Combine decoded passwords → create candidate for Cosmic Duality
- [ ] Try OpenSSL decryption with candidates
- [ ] Get "good" decryption → no "bad decrypt" error
- [ ] Read decrypted content → private key or next stage
- [ ] Celebrate! 🎉

---

## 💡 Pro Tips

1. **Save early, save often** - Keep copies of decoded sections
2. **Log everything** - Write down what works/doesn't work
3. **Try variations** - Spaces, hyphens, case variations
4. **Use pipes** - Test output immediately: `openssl ... | head -20`
5. **Trust the process** - The puzzle creator said it's solvable!
6. **Check your work** - Decoded text should be readable
7. **Don't give up** - The hardest part is the last 5% of passwords

---

**Last Updated:** January 2026  
**Status:** Final phase passwords unknown, everything else documented  
**Difficulty:** Medium-Hard  
**Time Required:** 2-5 hours  
**Good Luck!** 🔐

