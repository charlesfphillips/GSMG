# GSMG 5 BTC Puzzle - Complete Guide

## Overview
- **Original Prize**: 5 BTC (reduced to 2.5 BTC after first Bitcoin halving on May 11, 2020)
- **Prize Address**: `1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe`
- **Puzzle URL**: https://gsmg.io/puzzle
- **Community**: Reddit discussions on r/gsmgio_5_btc_puzzle

---

## Phase 1: Binary Matrix Steganography

### The Challenge
A 14×14 binary matrix where:
- Black/Blue squares = '1'
- Yellow/White squares = '0'

### Solution Method
1. Start from upper left corner
2. Move counterclockwise in a spiral pattern
3. Extract 8-bit sequences
4. Convert each byte to ASCII

### Result
**gsmg.io/theseedisplanted**

---

## Phase 2: Image Analysis & Hidden Form

### URL
https://gsmg.io/theseedisplanted

### Content: theseedisplanted.png
Images reference **"The Warning" by Logic**:
- Rearrange to see: WAR + NING
- Also: LO + (crypto)GIC

### Hidden Element
A POST form in HTML (accessible via browser F12 debug mode)

### Password
`theflowerblossomsthroughwhatseemstobeaconcretesurface`

### Next Step
Submit the form to advance

---

## Phase 3: The Matrix Reference & AES Decryption

### URL
https://gsmg.io/choiceisanillusioncreatedbetweenthosewithpowerandthosewithout

### Content: phase2.png
Movie quote from **The Matrix Reloaded**:

> **Merovingian**: "Choice is an illusion created between those with power and those without."

### Password Discovery
The password is: **causality**

### Decryption Command
```bash
SHA256(causality) = eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf

openssl enc -aes-256-cbc -d -a -in phase2.txt -pass pass:eb3efb5151e6255994711fe8f2264427ceeebf88109e1d7fad5b0a8b6d07e5bf
```

### Decrypted Message
References to **Thales Hardware Security Module** (HSM):
- 2name → Safenet
- 3Moon → Luna
- 4How so mate → HSM

**Hints encoded in the text include:**
- Mention of "keymakers" and "security by hiding"
- References to cryptographic concepts
- The phrase "in the worst gear"

---

## Phase 3.1: Seven-Part Password Construction

The decrypted content provides 7 parts to concatenate:

### Part 1: causality
Direct from previous phase

### Part 2: Safenet
From "2name" → Hardware security module brand

### Part 3: Luna
From "3Moon" → HSM product line

### Part 4: HSM
From "4How so mate" → Hardware Security Module

### Part 5: 11110
**Discovery Method**:
- References to **Norton's theorem** (electrical engineering)
- "4 rulers with first name of competition" → 4 US Presidents named "John"
  - John Adams
  - John Quincy Adams
  - John F. Kennedy
  - John Tyler
- "2 had firstname in surname" → Johnson (Andrew Johnson, Lyndon B. Johnson)
- JFK reference → Executive Order 11110 (related to Federal Reserve)
- 5-digit binary code: **11110**

### Part 6: 0x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854
**Source**: Line 1616 from Bitcoin's genesis block (main.cpp)
- This is raw hexadecimal data
- **Important**: Keep the casing (aBa) and remove whitespace

### Part 7: B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1
**Discovery Method**:
- Chess position puzzle: "A buddhist is forced to move"
- Buddhist move = non-violent, doesn't result in mate
- Solution position after the move
- **Important**: Keep casing and whitespace this time (connected NOT enf)

### Concatenation & Final Hash
```
Concatenate all 7 parts:
causalitySafenetLunaHSM111100x736B6E616220726F662074756F6C69616220646E6F63657320666F206B6E697262206E6F20726F6C6C65636E61684320393030322F6E614A2F33302073656D695420656854B5KR/1r5B/2R5/2b1p1p1/2P1k1P1/1p2P2p/1P2P2P/3N1N2 b - - 0 1

SHA256 = 1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
```

### Decrypt Phase 3
```bash
openssl enc -aes-256-cbc -d -a -in phase3.txt -pass pass:1a57c572caf3cf722e41f5f9cf99ffacff06728a43032dd44c481c77d2ec30d5
```

---

## Phase 3.2: The Architect's Message

### Encrypted Content
Large base64-encoded AES-256-CBC blob

### Password Discovery
Three clues combined:
1. **Jacque Fresco quote**: "The future is fluid..."
   - Answer: `jacquefresco`

2. **Alice & White Rabbit (Alice in Wonderland)**: "How long is forever? Sometimes, just one second."
   - Answer: `giveit` + `justonesecond`

3. **Heisenberg Uncertainty Principle**
   - Answer: `heisenbergsuncertaintyprinciple`

### Full Password
```
jacquefrescogiveitjustonesecondheisenbergsuncertaintyprinciple

SHA256 = 250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c
```

### Decryption Command
```bash
openssl enc -aes-256-cbc -d -a -in phase3.2.txt -pass pass:250f37726d6862939f723edc4f993fde9d33c6004aab4f2203d9ee489d61ce4c
```

### Decrypted Content
Contains:
- Matrix quote: "Why am I here? Wake up, Neo" (becomes "Wake up, you")
- "Beautiful strategic position" → Beaufort cipher hint
- "One for one, four for one" → 1141 encoding (IBM EBCDIC)
- Two encrypted segments with box drawing characters

---

## Phase 3.2.1: Beaufort Cipher Decryption

### Garbled Text (Box Drawing Characters)
Converted to letters: starts with "vtkvplmepphluwahtzmjpfipuxohaptukzztgikfwpuyatowynlebtqwffvgaaaxjflrxvokligooxeiexjywwukuucdlfwpwekogsngbvtzmnteulhpuchmrabiiejptvcaqbspqauhpmdjqhaqhuyddiwgxvxgpofaqizsentyesqmgchuazmyhmnrbzioyhucvqzcfmwxotomoblfeblcngppselsnlwaehcnwxznaynaceazhfzeunpeewjvhjysqjpposalabzuaplpppteafvvnzpryhsnkjuxsmkubnnimopukojensnlfxfabgeujmyqbqwtnmzitbtqwukuwfnxmfpepxuiwuxqqvgwgpzpptnguyaloavsnkppuhohkcazrghmrpbhicegsjdntttepqdmzrkdbstiabnasjmytghqhimcadgjvlhuvqaaababytxqhetvnpsknbinpxxwzrkfczjmhphezjmydkqtqrixlyhdolhuocpoecwakafomluodaoxmhxkiehekgkituelmynbpuhovoblpiyjakbduxbulpfnntcfmpqdsfdkcavazhakiepelyvabbkoitycfvushkbcjwzuadivfmgjdmbawzhmnekelhuocpykuhmnxiniregjqzlenbyexemnpucaleeiajvrjmyhdmodleopqkqnnzqbootnqmcybmdiajxmrdmmnqybgtllqkcizuihmjqpviehxwatlipitudotsfqgzmakmhnpqzinyxtzogygigvtmwbtghlpxttpgifohsgempkpiyatudomayqtzwtutlymtwppubmtwwuhmnwjphdhkrlflmzinushphruituniiedvfdirevdpplmibxrtehlqwylwtzmaqeeawhywbazsismrntewafxgvdbmjpzpmdiagaaihrjsmrntgwqkcqpkciwqjvrwcotjmrzazhtyaeototuhrowynfmpqdceegcgtitmcnpdqnzkvnppqsjrngjewaydjflwzutyelsmbyxwqzmuwhjvxoselapaaakmqnkjntejkpzwtoytarzqwklwqcowzuakeiqsgunubzcuaoyegltkwhwfniepiqegdkyqxqqoquwingecjemazpqlqwgykeajoummeaavibjledwfubscjptsfeqxuxehwqydrenanrelsfulftpmqmcoqetvkllbmdekhzrxiqsxyvqjdgzmanpqhhsnwgsqktwodrvznmmgomodijpbopqwptominnihfpulspucgbmoxeieauvdiacgjiqaugiyakhysfosijmasrzkfowgwxubauepijvrjmyhsmiwpyepamqzylwaaewajelybeawobvqcvwzaajuktvukudxztbhfgacdafvsmiwkbhlfiedpuhkczwlenaketkhklmbltryvaketuhkhkhppmyvvdogpwhtwqicyymqgovxnodkdaaabwbzagdahnqnfsaomzaeeawelkslhqlwigij"

### Beaufort Cipher Setup
**Password**: `THEMATRIXHASYOU`

**Alphabet Key** (from hint "fubcd-king & oracle-queen, thingky mvps"):
```
FUBCDORA.LETHINGKYMVPS.JQZXW
```

### Decoded Message
Key quote about the nature of the puzzle and a message from the creators encouraging solving it to help build something rather than chasing worthless prizes.

---

## Phase 3.2.2: VIC Cipher Decryption

### Cipher Number
```
15165943121972409169171213758951813141543131412428154191312181219433121171617137149110916631213131281491109166131412199114371612126021664313711154112
```

### VIC Cipher Parameters
- **Alphabet hint**: "fubcd-king & oracle-queen, thingky mvps"
- Removing repeats: `FUBCDORA.LETHINGKYMVPS.JQZXW`
- **Digit mapping**: digit 1 = 1, digit 2 = 4

### Online Tool
Use: https://www.dcode.fr/vic-cipher

### Decoded Result
```
IN CASE YOU MANAGE TO CRACK THIS THE PRIVATE KEYS BELONG TO HALF AND BETTER HALF AND THEY ALSO NEED FUNDS TO LIVE
```

---

## Additional Hints from Creator

### Decentraland Hint
- Find coordinates in Decentraland
- Extract audio file
- Process: Split stereo → Invert one channel → Mix stereo → Downmix to mono → Create spectrogram
- **Answer**: `HASHTHETEXT`

### Nursery Rhyme Hint
```
Roses are White but often Red.
Yellow has a number and so does Blue.
Go back to the first puzzle piece without further ado.

It might have shown you only one door, beware that the rabbits nest may contain a whole lot more.

Hush hush.
```

### First Puzzle Piece Hash
```
SHA256(GSMGIO5BTCPUZZLECHALLENGE1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe)
= 89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32
```

---

## Salphaseion (Hidden Phase)

### URL
https://gsmg.io/89727c598b9cd1cf8873f27cb7057f050645ddb6a7a157a110239ac0152f6a32

### Current Status
This phase contains multiple encoded sections, some partially decoded:

#### ABBA Binary Sections
Convert a=0, b=1 to binary, then to ASCII:
- Section 1: `"matrixsumlist"`
- Section 2: `"enter"`

#### Hexadecimal Encoded Sections
Using a=1...z=26 with 'o'=0, convert to base 16, then decode as ASCII hex:
- Section 1: `"lastwordsbeforearchichoice"`
- Section 2: `"thispassword"`

#### AES Blob (Salphaseion)
```
U2FsdGVkX18...
```
(Final encrypted segment - decryption key unknown or not yet published)

---

## Tools & Resources

### Online Decoders
- **SHA256**: https://xorbin.com/tools/sha256-hash-calculator
- **Beaufort Cipher**: https://ciphertools.co.uk/decode.php
- **VIC Cipher**: https://www.dcode.fr/vic-cipher
- **OpenSSL** (local): For AES decryption

### OpenSSL Commands Reference
```bash
# AES-256-CBC Decryption
openssl enc -aes-256-cbc -d -a -in <filename> -pass pass:<sha256_hash>

# Key flags:
# -d          = decrypt
# -a          = data is base64 encoded
# -in         = input file
# -out        = output file
# -pass pass: = password (as text or SHA256 hash)
```

---

## Summary of Techniques Used

1. **Binary Steganography** - Hidden message in bit matrix
2. **Web Exploration** - Hidden HTML forms
3. **Image Analysis** - Visual references to media
4. **Cryptographic Hashing** - SHA256 for passwords
5. **AES-256-CBC Encryption** - Symmetric encryption
6. **Beaufort Cipher** - Classical cipher method
7. **VIC Cipher** - Complex classical cipher
8. **Chess Notation** - Puzzle logic
9. **Reference Decoding** - Cultural/movie knowledge
10. **Audio Steganography** - Spectrogram extraction
11. **Number Systems** - Binary, Hex, Base conversions
12. **Literary Analysis** - Quotes and hidden meanings

---

## Creator's Message

The puzzle emphasizes that the real value isn't in winning worthless prizes, but in being part of building something meaningful. The creators encourage solvers to help them accomplish their goals rather than just hunting for trophies.

**Final Note**: "I really hope you're the one. Ciao bella."
