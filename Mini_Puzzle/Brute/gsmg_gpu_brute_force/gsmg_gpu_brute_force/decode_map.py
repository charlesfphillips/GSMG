#!/usr/bin/env python3
import binascii

# Replace these with the exact strings from Salphaseion if different
s1 = "agdafaoaheiecggchgicbbhcgbehcfcoabicfdhhcdbbcagbdaiobbgbeadedde"
s2 = "cfobfdhgdobdgooiigdocdaoofidh"

mapping = {'a':'1','b':'2','c':'3','d':'4','e':'5','f':'6','g':'7','h':'8','i':'9','o':''}

def map_to_decimal(s):
    return ''.join(mapping.get(ch, '?') for ch in s)

def dec_to_hex_ascii(decstr):
    try:
        n = int(decstr)
    except Exception:
        return None, None
    hx = format(n, 'x')
    if len(hx) % 2 == 1:
        hx = '' + hx
    try:
        txt = binascii.unhexlify(hx).decode('utf-8', errors='replace')
    except Exception:
        txt = None
    return hx, txt

def chunk_decimal_to_ascii(decstr):
    results = set()
    L = len(decstr)
    for chunk_size in (2, 3):
        i = 0
        out = []
        ok = True
        while i < L:
            chunk = decstr[i:i+chunk_size]
            if len(chunk) < chunk_size:
                ok = False
                break
            try:
                val = int(chunk)
            except:
                ok = False
                break
            if val < 32 or val > 126:
                ok = False
                break
            out.append(chr(val))
            i += chunk_size
        if ok:
            results.add(''.join(out))
    return results

def try_variants(name, s):
    dec = map_to_decimal(s)
    print(f"\n{name} mapped decimal (len {len(dec)}):\n{dec}\n")
    variants = [
        ('as_is', dec),
        ('append_1106', dec + '1106'),
    ]
    try:
        variants.append(('add_1106_numeric', str(int(dec) + 1106)))
    except Exception:
        pass

    for vname, v in variants:
        hx, txt = dec_to_hex_ascii(v)
        print(f"Variant {vname}: hex start: {hx[:120] if hx else '<<no hex>>'} ...")
        print(f" Variant {vname}: ascii (hex->ascii) start: {txt[:200] if txt else '<<no ascii>>'}")
        chunks = chunk_decimal_to_ascii(v)
        if chunks:
            print(f" Variant {vname}: chunked-decimal ASCII candidates: {chunks}")
        else:
            print(f" Variant {vname}: chunked-decimal ASCII candidates: none")

    # raw big-endian bytes view
    try:
        n = int(dec)
        raw = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        print(f" Raw bytes (len {len(raw)}) hex start: {raw[:64].hex()}")
        try:
            print(" Raw bytes utf8 start:", raw[:200].decode('utf-8', errors='replace'))
        except Exception:
            pass
    except Exception as e:
        print("Could not convert to raw bytes:", e)

if __name__ == '__main__':
    try_variants("section1", s1)
    try_variants("section2", s2)