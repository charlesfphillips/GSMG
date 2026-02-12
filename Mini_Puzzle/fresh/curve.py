import hashlib

# Curve order for secp256k1
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def solve_vanity_sum(k1_hex, k2_hex, mode='add'):
    # Convert hex keys to integers
    k1_int = int(k1_hex, 16)
    k2_int = int(k2_hex, 16)
    
    if mode == 'add':
        # Standard Cosmic Duality Sum
        final_int = (k1_int + k2_int) % N
    else:
        # The "Negative Key" Trick
        final_int = (k1_int - k2_int) % N
        
    return hex(final_int)

# Example usage (Replace with your actual decoded hex values)
# k1_hex = "..." 
# k2_hex = "..."
# print(solve_vanity_sum(k1_hex, k2_hex))