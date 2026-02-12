import hashlib
import subprocess

# Expanded candidates focusing on "1name" (First Name) and "Works"
candidates = [
    "giveitWerner",
    "giveitHeisenberg",
    "giveitUncertainty",
    "giveitwerner",
    "giveitwernerheisenberg",
    "giveitWernerHeisenberg",
    "giveituncertaintyprinciple",
    "giveitmatrixmechanics", # Heisenberg's specific 'work'
    "giveit1name", # Literal interpretation
    "giveitjustasecond" # Alice variation
]

def try_decrypt(password_str):
    pw_hash = hashlib.sha256(password_str.encode()).hexdigest()
    cmd = [
        "openssl", "enc", "-aes-256-cbc", "-d", "-a", 
        "-in", "phase3_2.txt", "-pass", f"pass:{pw_hash}"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True)
        if b"bad decrypt" not in result.stderr.lower() and result.returncode == 0:
            return pw_hash, result.stdout
    except:
        pass
    return None, None

print("Hunting for the '1name' match...")
for c in candidates:
    print(f"Testing: {c:25}", end="\r")
    pw, output = try_decrypt(c)
    if pw:
        print(f"\n\nSUCCESS! Password string: {c}")
        print(f"SHA256 Hash: {pw}")
        with open("REVEALED_3_2.bin", "wb") as f:
            f.write(output)
        break
else:
    print("\nNo matches found. Checking if the hash itself is the password...")