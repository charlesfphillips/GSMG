n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def to_int(h): return int(h, 16)

a = to_int("8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af")
b = to_int("d12f8b341cb879dd769ade1f8d399d40ae27695b880aa5701df9abd8c96387cd")

add = (a + b) % n
sub = (a - b) % n
xor = a ^ b

print(f"Add hex: {hex(add)[2:].zfill(64)}")
print(f"Sub hex: {hex(sub)[2:].zfill(64)}")
print(f"XOR hex: {hex(xor)[2:].zfill(64)}")