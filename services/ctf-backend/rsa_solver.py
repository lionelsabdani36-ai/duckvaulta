#!/usr/bin/env python3
import re
import math
import gmpy2
import sympy
import requests
from Crypto.Util.number import long_to_bytes, bytes_to_long

FLAG_REGEX = re.compile(r'(?:GETSFLAG|picoCTF|pico|FLAG|flag|CTF|HTB|THM)\{[^{}\n]{1,80}\}')

def hunt_flag(text):
    if not text:
        return None
    m = FLAG_REGEX.search(text)
    return m.group(0) if m else None

def parse_rsa_input(text):
    params = {}
    lines = text.splitlines()
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'([a-zA-Z0-9_]+)\s*[:=]\s*([0-9a-fA-FxX]+)', line)
        if m:
            k = m.group(1).lower()
            val_str = m.group(2).strip()
            try:
                if val_str.startswith(('0x', '0X')):
                    val = int(val_str, 16)
                else:
                    val = int(val_str)
                params[k] = val
            except ValueError:
                pass

    # Normalize keys
    norm = {}
    if 'n' in params: norm['n'] = params['n']
    elif 'modulus' in params: norm['n'] = params['modulus']

    if 'e' in params: norm['e'] = params['e']
    elif 'exp' in params or 'exponent' in params: norm['e'] = params.get('exp') or params.get('exponent')
    else: norm['e'] = 65537

    if 'c' in params: norm['c'] = params['c']
    elif 'ct' in params or 'ciphertext' in params: norm['c'] = params.get('ct') or params.get('ciphertext')

    if 'p' in params: norm['p'] = params['p']
    if 'q' in params: norm['q'] = params['q']
    if 'd' in params: norm['d'] = params['d']
    if 'phi' in params: norm['phi'] = params['phi']
    if 'dp' in params: norm['dp'] = params['dp']
    if 'dq' in params: norm['dq'] = params['dq']

    # Multiple pairs
    for k in ['n1', 'c1', 'e1', 'n2', 'c2', 'e2', 'n3', 'c3', 'e3']:
        if k in params:
            norm[k] = params[k]

    return norm

def decode_message(m_int):
    try:
        raw_bytes = long_to_bytes(int(m_int))
        # try utf-8
        try:
            txt = raw_bytes.decode('utf-8')
        except UnicodeDecodeError:
            txt = "".join(chr(b) if 32 <= b <= 126 or b in (10, 13, 9) else '.' for b in raw_bytes)
        return {
            "text": txt,
            "hex": hex(int(m_int)),
            "flag": hunt_flag(txt)
        }
    except Exception as err:
        return {
            "text": str(m_int),
            "hex": hex(int(m_int)),
            "flag": None
        }

def solve_fermat(n, max_iter=2000000):
    a, exact = gmpy2.iroot(n, 2)
    if not exact:
        a += 1
    for _ in range(max_iter):
        b2 = a * a - n
        b, is_sq = gmpy2.iroot(b2, 2)
        if is_sq:
            p = int(a - b)
            q = int(a + b)
            if p * q == n and p > 1:
                return p, q
        a += 1
    return None

def solve_wiener(n, e):
    # Continued fractions of e/n
    a, b = e, n
    cf = []
    while b != 0:
        cf.append(a // b)
        a, b = b, a % b

    p0, p1 = 0, 1
    q0, q1 = 1, 0
    for q_k in cf:
        p_new = q_k * p1 + p0
        q_new = q_k * q1 + q0
        p0, p1 = p1, p_new
        q0, q1 = q1, q_new
        k = p1
        d = q1
        if k == 0:
            continue
        if (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            b_val = n - phi + 1
            disc = b_val * b_val - 4 * n
            if disc >= 0:
                s, exact = gmpy2.iroot(disc, 2)
                if exact:
                    p = (b_val + s) // 2
                    q = (b_val - s) // 2
                    if p * q == n:
                        return int(d), int(p), int(q)
    return None

def solve_small_e(c, e, n, max_k=500):
    for k in range(max_k + 1):
        target = c + k * n
        m, exact = gmpy2.iroot(target, e)
        if exact:
            return int(m)
    return None

def solve_pollard_p1(n, B=100000):
    a = 2
    for j in range(2, B):
        a = pow(a, j, n)
        d = math.gcd(a - 1, n)
        if 1 < d < n:
            return d, n // d
    return None

def solve_factordb(n):
    try:
        url = f"https://factordb.com/api?query={n}"
        res = requests.get(url, timeout=3.5)
        if res.status_code == 200:
            data = res.json()
            status = data.get('status')
            if status in ['FF', 'CF']:
                factors = data.get('factors', [])
                primes = []
                for f, count in factors:
                    for _ in range(count):
                        primes.append(int(f))
                if len(primes) >= 2:
                    return primes[0], n // primes[0]
    except Exception:
        pass
    return None

def solve_common_modulus(n, e1, c1, e2, c2):
    def egcd(a, b):
        if b == 0:
            return 1, 0, a
        x1, y1, d = egcd(b, a % b)
        return y1, x1 - (a // b) * y1, d

    s, t, g = egcd(e1, e2)
    if g != 1 and g != -1:
        return None
    if s < 0:
        c1_inv = int(gmpy2.invert(c1, n))
        term1 = pow(c1_inv, -s, n)
    else:
        term1 = pow(c1, s, n)

    if t < 0:
        c2_inv = int(gmpy2.invert(c2, n))
        term2 = pow(c2_inv, -t, n)
    else:
        term2 = pow(c2, t, n)

    m = (term1 * term2) % n
    return m

def solve_rsa_auto(params):
    n = params.get('n')
    e = params.get('e', 65537)
    c = params.get('c')
    p = params.get('p')
    q = params.get('q')
    d = params.get('d')
    phi = params.get('phi')
    dp = params.get('dp')
    dq = params.get('dq')

    # Common modulus check
    if 'n1' in params and 'c1' in params and 'e1' in params and 'e2' in params and 'c2' in params:
        m = solve_common_modulus(params['n1'], params['e1'], params['c1'], params['e2'], params['c2'])
        if m:
            dec = decode_message(m)
            return {
                "success": True,
                "data": {
                    "method": "Common Modulus Attack (n sama, 2 pasang e/c)",
                    "plaintext": dec["text"],
                    "flag": dec["flag"],
                    "decimal": str(m),
                    "hex": dec["hex"],
                    "n": str(params['n1']),
                    "e1": str(params['e1']),
                    "e2": str(params['e2'])
                }
            }

    if not n and not (p and q):
        return {"success": False, "message": "Modulus n tidak ditemukan di input."}

    # Case 1: p and q known
    if p and q:
        n = p * q
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        if c:
            m = pow(c, d, n)
            dec = decode_message(m)
            return {
                "success": True,
                "data": {
                    "method": "Given Primes (p, q)",
                    "plaintext": dec["text"],
                    "flag": dec["flag"],
                    "decimal": str(m),
                    "hex": dec["hex"],
                    "p": str(p),
                    "q": str(q),
                    "d": str(d),
                    "phi": str(phi)
                }
            }

    # Case 2: d known
    if d and c and n:
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "Given Private Exponent (d)",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "d": str(d)
            }
        }

    # Case 3: phi known
    if phi and c and n:
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "Given Euler Totient (phi)",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "d": str(d),
                "phi": str(phi)
            }
        }

    # Case 4: dp known (CRT)
    if dp and p and c:
        m = pow(c, dp, p)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "Chinese Remainder Theorem (dp = d mod p-1)",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"]
            }
        }

    if not c:
        return {"success": False, "message": "Ciphertext c tidak ditemukan di input."}

    # Case 5: Small exponent root
    if e < 30:
        m = solve_small_e(c, e, n, max_k=300)
        if m:
            dec = decode_message(m)
            return {
                "success": True,
                "data": {
                    "method": f"Small Exponent Attack (e={e}, integer root)",
                    "plaintext": dec["text"],
                    "flag": dec["flag"],
                    "decimal": str(m),
                    "hex": dec["hex"]
                }
            }

    # Case 6: Fermat Factorization
    fermat_res = solve_fermat(n)
    if fermat_res:
        p, q = fermat_res
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "Fermat Factorization (Prima p & q berdekatan)",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "p": str(p),
                "q": str(q),
                "d": str(d),
                "phi": str(phi)
            }
        }

    # Case 7: Wiener Attack
    wiener_res = solve_wiener(n, e)
    if wiener_res:
        d, p, q = wiener_res
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "Wiener Attack (Small Private Exponent d)",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "p": str(p),
                "q": str(q),
                "d": str(d)
            }
        }

    # Case 8: Small Prime Factorization
    small_p = None
    for p_cand in sympy.primerange(2, 500000):
        if n % p_cand == 0:
            small_p = int(p_cand)
            break
    if small_p:
        p = small_p
        q = n // p
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": f"Trial Division (Faktor prima kecil: {p})",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "p": str(p),
                "q": str(q),
                "d": str(d)
            }
        }

    # Case 9: Pollard p-1
    pollard_res = solve_pollard_p1(n, B=80000)
    if pollard_res:
        p, q = pollard_res
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "Pollard's p-1 Factorization (p-1 smooth)",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "p": str(p),
                "q": str(q),
                "d": str(d)
            }
        }

    # Case 10: FactorDB Online
    fdb_res = solve_factordb(n)
    if fdb_res:
        p, q = fdb_res
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return {
            "success": True,
            "data": {
                "method": "FactorDB Database Factorization",
                "plaintext": dec["text"],
                "flag": dec["flag"],
                "decimal": str(m),
                "hex": dec["hex"],
                "p": str(p),
                "q": str(q),
                "d": str(d)
            }
        }

    return {
        "success": False,
        "message": "Auto-detect mencoba Fermat, Wiener, Small e, Pollard p-1, Small Primes, dan FactorDB namun n tidak dapat difaktorkan secara instan. Coba gunakan tools eksternal (SageMath/Alpertron) di tab Referensi."
    }
