import hashlib
import subprocess

# All decoded passwords we have
passwords = [
    "matrixsumlist",
    "enter",
]

print("="*80)
print("COMPREHENSIVE PASSWORD TESTING")
print("="*80)

# Try all combinations
candidates = []

# Individual
for p in passwords:
    candidates.append(p)

# Pairs
candidates.append("matrixsumlist" + "enter")
candidates.append("enter" + "matrixsumlist")

# With spaces/separators
for sep in ["", "_", "-", " "]:
    candidates.append(sep.join(passwords))

# SHA256 hashes of above
for cand in list(candidates):
    candidates.append(hashlib.sha256(cand.encode()).hexdigest())

print(f"\nTotal candidates to test: {len(set(candidates))}\n")

# Test with OpenSSL
cosmic = open('/home/claude/cosmic_duality_real.txt', 'r').read()

for cand in set(candidates):
    try:
        proc = subprocess.Popen(
            ['openssl', 'enc', '-aes-256-cbc', '-d', '-a', '-pass', f'pass:{cand}'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = proc.communicate(input=cosmic, timeout=2)
        
        if proc.returncode == 0 and stdout and "bad decrypt" not in stderr:
            print(f"\n✓✓✓ SUCCESS! ✓✓✓")
            print(f"Password: {cand}")
            print(f"\nDecrypted content:")
            print("="*80)
            print(stdout[:500])
            print("="*80)
            
            # Save full result
            open('/tmp/SOLUTION_FOUND.txt', 'w').write(stdout)
            break
    except Exception as e:
        pass

