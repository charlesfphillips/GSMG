import re

def hunt_for_1106(file_path):
    with open(file_path, 'r') as f:
        content = f.read()

    # Find all textareas
    textareas = re.findall(r'<textarea[^>]*>(.*?)</textarea>', content, re.DOTALL)
    
    for i, text in enumerate(textareas):
        # Clean text to just letters
        letters = [char.lower() for char in text if char.isalpha()]
        
        # Test sliding windows of 196 letters
        for start in range(len(letters) - 195):
            window = letters[start:start+196]
            current_sum = sum(ord(c) - ord('a') + 1 for c in window)
            
            if current_sum == 1106:
                print(f"FOUND 1106! Textarea index: {i}, Start letter index: {start}")
                print(f"First 10 letters of grid: {''.join(window[:10])}")
                return
                
    print("Could not find any sequence of 196 letters summing to 1106.")

if __name__ == "__main__":
    hunt_for_1106("GSMG Puzzle.htm")