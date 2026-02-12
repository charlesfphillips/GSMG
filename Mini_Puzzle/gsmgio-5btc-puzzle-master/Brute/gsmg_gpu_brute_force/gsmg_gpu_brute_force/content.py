S2 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"
mapping = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','o':'0'}
s2_digits = "".join(mapping[char] for char in S2)
n1 = int(s2_digits)

# Convert to hex and then to string
hex_val = hex(n1)[2:]
try:
    decoded_text = bytes.fromhex(hex_val).decode('utf-8')
    print(f"Section 2 Decoded: {decoded_text}")
except:
    print(f"Section 2 Hex: {hex_val}")