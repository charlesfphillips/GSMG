# Theoretical 1/30 Reconstruction
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
inv2 = pow(2, -1, N)

half_a = int("8badeb454dbeb5d2263d8774b8b24f1bd14fd658bc7635cab922f80d5a7b54af", 16)
halved_a = (half_a * inv2) % N

# We need THIS value from your LK file:
# better_half = int("HEX_FROM_LK_FILE", 16) 

# master_int = (halved_a + better_half + 1106) % N