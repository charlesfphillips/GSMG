import re

def build_final_grid():
    try:
        # 1. Load the file containing the raw SalPhaseIon letters
        # Do NOT use the encrypted 'cosmic_duality_real_CORRECT.txt'
        with open('salphaseion.txt', 'r') as f:
            data = f.read().lower()

        # 2. Extract only the valid puzzle characters
        clean_string = "".join(c for c in data if c in 'abcdefghioz')
        
        # 3. Handle English hints often found in the block
        hints = ['shabefourfirsthintisyourlastcommand', 'shabefanstoo']
        for hint in hints:
            clean_string = clean_string.replace(hint, '')

        length = len(clean_string)
        target = 10609

        print(f"Cleaned String Length: {length}")

        if length >= target:
            if length > target:
                print(f"Trimming {length - target} extra characters...")
                clean_string = clean_string[:target]
            
            # Build 103x103 grid
            grid = [clean_string[i*103:(i+1)*103] for i in range(103)]
            with open('grid_103x103.txt', 'w') as f_out:
                for row in grid:
                    f_out.write(row + '\n')
            print("SUCCESS: 103x103 grid saved to grid_103x103.txt")
        else:
            print(f"FAILED: Only {length} characters found. You are missing {target - length} chars.")

    except FileNotFoundError:
        print("Error: Please save the SalPhaseIon letters into 'salphaseion.txt' first.")

if __name__ == "__main__":
    build_final_grid()