from bip32utils import BIP32Key
import binascii

# 1. THE SEED (From your successful 'Bella Ciao' 128-bit entropy)
# Based on the signpost proof:
seed_hex = "8badeb454dbeb5d2263d8774b8b24f1b"
seed = binascii.unhexlify(seed_hex)

# 2. THE DERIVATION
# Root -> Purpose (44') -> Coin (0') -> Account (0') -> Chain (0) -> Index (12)
root = BIP32Key.fromEntropy(seed)
child = root.ChildKey(44 + 0x80000000).ChildKey(0 + 0x80000000).ChildKey(0 + 0x80000000).ChildKey(0).ChildKey(12)

print(f"Index 12 Private Key (Hex): {child.PrivateKey().hex()}")
print(f"Index 12 Address: {child.Address()}")
print("-" * 30)
print(f"WIF: {child.WalletImportFormat()}")