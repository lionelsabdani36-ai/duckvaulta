#!/usr/bin/env python3
import re
import math
import random
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
    multi_primes = []
    lines = text.splitlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # Check for list of primes: primes = [...] or primes: [...]
        list_match = re.search(r'(?:primes|factors)\s*[:=]\s*\[([^\]]+)\]', line, re.I)
        if list_match:
            raw_nums = list_match.group(1).split(',')
            for item in raw_nums:
                item = item.strip()
                try:
                    multi_primes.append(int(item, 16 if item.startswith(('0x', '0X')) else 10))
                except ValueError:
                    pass
            continue

        # Match key = val or key : val or key = 0x...
        # Also supports greek letters φ and variables like phi(n)
        m = re.match(r'([a-zA-Z0-9_φΦ()]+)\s*[:=]\s*([0-9a-fA-FxX]+)', line)
        if m:
            k = m.group(1).lower().replace('(', '').replace(')', '')
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
    elif 'mod' in params: norm['n'] = params['mod']

    if 'e' in params: norm['e'] = params['e']
    elif 'exp' in params or 'exponent' in params: norm['e'] = params.get('exp') or params.get('exponent')
    elif 'pubexp' in params: norm['e'] = params['pubexp']
    else: norm['e'] = 65537

    if 'c' in params: norm['c'] = params['c']
    elif 'ct' in params or 'ciphertext' in params: norm['c'] = params.get('ct') or params.get('ciphertext')
    elif 'cipher' in params: norm['c'] = params['cipher']

    if 'p' in params: norm['p'] = params['p']
    elif 'prime1' in params: norm['p'] = params['prime1']
    elif 'p1' in params: norm['p'] = params['p1']

    if 'q' in params: norm['q'] = params['q']
    elif 'prime2' in params: norm['q'] = params['prime2']
    elif 'p2' in params: norm['q'] = params['p2']

    if 'r' in params: norm['r'] = params['r']
    elif 'prime3' in params: norm['r'] = params['prime3']
    elif 'p3' in params: norm['r'] = params['p3']

    if 'd' in params: norm['d'] = params['d']
    elif 'priv' in params or 'privkey' in params or 'private_key' in params:
        norm['d'] = params.get('priv') or params.get('privkey') or params.get('private_key')

    # Phi / Euler Totient detection
    for phi_key in ['phi', 'phin', 'totient', 'eulertotient', 'φ', 'Φ']:
        if phi_key in params:
            norm['phi'] = params[phi_key]
            break

    if 'dp' in params: norm['dp'] = params['dp']
    elif 'dmp1' in params: norm['dp'] = params['dmp1']

    if 'dq' in params: norm['dq'] = params['dq']
    elif 'dmq1' in params: norm['dq'] = params['dmq1']

    # Multiple pairs
    for k in ['n1', 'c1', 'e1', 'n2', 'c2', 'e2', 'n3', 'c3', 'e3']:
        if k in params:
            norm[k] = params[k]

    if multi_primes:
        norm['primes'] = multi_primes

    return norm

def check_truncation_warning(c, n, flag_found):
    if c and n and not flag_found:
        if c.bit_length() < n.bit_length() * 0.7:
            return f"Ciphertext c ({c.bit_length()} bit) jauh lebih kecil dari modulus n ({n.bit_length()} bit). Kemungkinan nilai c terpotong saat disalin dari soal CTF."
    return None

def decode_message(m_int):
    try:
        raw_bytes = long_to_bytes(int(m_int))
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

def format_result(method, m, n, c, dec, extra=None):
    res = {
        "method": method,
        "plaintext": dec["text"],
        "flag": dec["flag"],
        "decimal": str(m) if m is not None else None,
        "hex": dec["hex"],
    }
    if extra:
        res.update(extra)
    warn = check_truncation_warning(c, n, dec["flag"])
    if warn:
        res["warning"] = warn
    return {"success": True, "data": res}

def factor_n_with_d(n, e, d):
    """Miller's probabilistic algorithm to factor n using known e and d"""
    try:
        k = e * d - 1
        s = 0
        t = k
        while t % 2 == 0:
            s += 1
            t //= 2
        for _ in range(100):
            g = random.randint(2, n - 2)
            y = pow(g, t, n)
            if y == 1 or y == n - 1:
                continue
            for _ in range(1, s):
                x = pow(y, 2, n)
                if x == n - 1:
                    break
                if x == 1:
                    p_cand = math.gcd(y - 1, n)
                    if 1 < p_cand < n:
                        return p_cand, n // p_cand
                y = x
    except Exception:
        pass
    return None

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

def solve_small_e(c, e, n, max_k=1000):
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
    r = params.get('r')
    d = params.get('d')
    phi = params.get('phi')
    dp = params.get('dp')
    dq = params.get('dq')
    primes = params.get('primes', [])

    # Case 0: Common modulus attack
    if 'n1' in params and 'c1' in params and 'e1' in params and 'e2' in params and 'c2' in params:
        m = solve_common_modulus(params['n1'], params['e1'], params['c1'], params['e2'], params['c2'])
        if m:
            dec = decode_message(m)
            return format_result("Common Modulus Attack (n sama, 2 pasang e/c)", m, params['n1'], params['c1'], dec, {
                "n": str(params['n1']), "e1": str(params['e1']), "e2": str(params['e2'])
            })

    # Case 1: Trivial e = 1 (c = m)
    if e == 1 and c is not None:
        m = c if not n else (c % n)
        dec = decode_message(m)
        return format_result("Trivial RSA (e = 1, Ciphertext = Plaintext)", m, n, c, dec)

    # Case 2: Multi-Prime RSA (n = p * q * r ... or primes list given)
    all_primes = list(primes)
    if p: all_primes.append(p)
    if q: all_primes.append(q)
    if r: all_primes.append(r)
    # Deduplicate while preserving order
    unique_primes = []
    for pr in all_primes:
        if pr not in unique_primes:
            unique_primes.append(pr)

    if len(unique_primes) >= 3 and c:
        calc_n = 1
        calc_phi = 1
        for pr in unique_primes:
            calc_n *= pr
            calc_phi *= (pr - 1)
        use_n = n or calc_n
        d_val = int(gmpy2.invert(e, calc_phi))
        m = pow(c, d_val, use_n)
        dec = decode_message(m)
        return format_result(f"Multi-Prime RSA ({len(unique_primes)} faktor prima)", m, use_n, c, dec, {
            "n": str(use_n), "d": str(d_val), "phi": str(calc_phi),
            "primes": ", ".join(str(pr) for pr in unique_primes)
        })

    # Case 3: Both p and q known
    if p and q:
        n = p * q
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        if c:
            m = pow(c, d, n)
            dec = decode_message(m)
            return format_result("Given Primes (p, q)", m, n, c, dec, {
                "p": str(p), "q": str(q), "d": str(d), "phi": str(phi)
            })

    # Case 4: Known Modulus n and single factor p or q
    # Check if p is provided with n
    if n and p and not q:
        if n % p == 0:
            q = n // p
            phi = (p - 1) * (q - 1)
            d = int(gmpy2.invert(e, phi))
            if c:
                m = pow(c, d, n)
                dec = decode_message(m)
                return format_result("Factor Given with Modulus n (q = n / p)", m, n, c, dec, {
                    "p": str(p), "q": str(q), "d": str(d), "phi": str(phi)
                })
        else:
            # HEURISTIC: What if p was actually phi(n)?
            # In RSA: phi = n - (p_real + q_real) + 1 => s = p_real + q_real = n - phi + 1
            s = n - p + 1
            if s > 0:
                disc = s * s - 4 * n
                if disc >= 0:
                    sq, exact = gmpy2.iroot(disc, 2)
                    if exact:
                        p_real = int((s - sq) // 2)
                        q_real = int((s + sq) // 2)
                        if p_real * q_real == n:
                            phi_val = p
                            d_val = int(gmpy2.invert(e, phi_val))
                            if c:
                                m = pow(c, d_val, n)
                                dec = decode_message(m)
                                return format_result("Given Euler Totient phi (Parameter berlabel p terdeteksi sebagai phi(n))", m, n, c, dec, {
                                    "p": str(p_real), "q": str(q_real), "d": str(d_val), "phi": str(phi_val)
                                })

    # Check if q is provided with n
    if n and q and not p:
        if n % q == 0:
            p = n // q
            phi = (p - 1) * (q - 1)
            d = int(gmpy2.invert(e, phi))
            if c:
                m = pow(c, d, n)
                dec = decode_message(m)
                return format_result("Factor Given with Modulus n (p = n / q)", m, n, c, dec, {
                    "p": str(p), "q": str(q), "d": str(d), "phi": str(phi)
                })
        else:
            # HEURISTIC: What if q was actually phi(n)?
            s = n - q + 1
            if s > 0:
                disc = s * s - 4 * n
                if disc >= 0:
                    sq, exact = gmpy2.iroot(disc, 2)
                    if exact:
                        p_real = int((s - sq) // 2)
                        q_real = int((s + sq) // 2)
                        if p_real * q_real == n:
                            phi_val = q
                            d_val = int(gmpy2.invert(e, phi_val))
                            if c:
                                m = pow(c, d_val, n)
                                dec = decode_message(m)
                                return format_result("Given Euler Totient phi (Parameter berlabel q terdeteksi sebagai phi(n))", m, n, c, dec, {
                                    "p": str(p_real), "q": str(q_real), "d": str(d_val), "phi": str(phi_val)
                                })

    # Case 5: Phi known explicitly
    if phi and c:
        d = int(gmpy2.invert(e, phi))
        extra = {"phi": str(phi), "d": str(d)}
        if n:
            m = pow(c, d, n)
            # Try to factor n as well via quadratic equation
            s = n - phi + 1
            if s > 0:
                disc = s * s - 4 * n
                if disc >= 0:
                    sq, exact = gmpy2.iroot(disc, 2)
                    if exact:
                        extra["p"] = str(int((s - sq) // 2))
                        extra["q"] = str(int((s + sq) // 2))
            dec = decode_message(m)
            return format_result("Given Euler Totient (phi)", m, n, c, dec, extra)

    # Case 6: Private Exponent d known
    if d and c and n:
        m = pow(c, d, n)
        dec = decode_message(m)
        extra = {"d": str(d)}
        # Try to factor n into p and q using Miller's algorithm
        factors = factor_n_with_d(n, e, d)
        if factors:
            extra["p"] = str(factors[0])
            extra["q"] = str(factors[1])
            extra["phi"] = str((factors[0] - 1) * (factors[1] - 1))
        return format_result("Given Private Exponent (d)", m, n, c, dec, extra)

    # Case 7: dp known (CRT)
    if dp and p and c:
        m = pow(c, dp, p)
        dec = decode_message(m)
        return format_result("Chinese Remainder Theorem (dp = d mod p-1)", m, n, c, dec, {"p": str(p), "dp": str(dp)})

    if not n:
        return {"success": False, "message": "Modulus n tidak ditemukan di input."}

    if not c:
        return {"success": False, "message": "Ciphertext c tidak ditemukan di input."}

    # Case: Power Modulus Attack (n = p^k, e.g. n = p^2, n = p^3)
    for k in range(2, 9):
        r, exact = gmpy2.iroot(n, k)
        if exact:
            p_root = int(r)
            phi_val = (p_root ** (k - 1)) * (p_root - 1)
            d_val = int(gmpy2.invert(e, phi_val))
            m = pow(c, d_val, n)
            dec = decode_message(m)
            return format_result(f"Square/Power Modulus Attack (n = p^{k})", m, n, c, dec, {
                "p": str(p_root),
                "k": str(k),
                "phi": str(phi_val),
                "d": str(d_val)
            })

    # Case: Prime Modulus (n is a prime, phi = n - 1)
    if sympy.isprime(n):
        phi_val = n - 1
        d_val = int(gmpy2.invert(e, phi_val))
        m = pow(c, d_val, n)
        dec = decode_message(m)
        return format_result("Prime Modulus Attack (n bilangan prima, phi = n - 1)", m, n, c, dec, {
            "phi": str(phi_val),
            "d": str(d_val)
        })

    # Case 8: Small Exponent root (e <= 17)
    if e <= 17:
        m = solve_small_e(c, e, n, max_k=1000)
        if m:
            dec = decode_message(m)
            return format_result(f"Small Exponent Attack (e={e}, integer root)", m, n, c, dec)

    # Case 9: Fermat Factorization (p ≈ q)
    fermat_res = solve_fermat(n, max_iter=2000000)
    if fermat_res:
        p, q = fermat_res
        phi = p * (p - 1) if p == q else (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return format_result("Fermat Factorization (Prima p & q berdekatan)", m, n, c, dec, {
            "p": str(p), "q": str(q), "d": str(d), "phi": str(phi)
        })

    # Case 10: Wiener Attack (Small d < 1/3 n^0.25)
    wiener_res = solve_wiener(n, e)
    if wiener_res:
        d, p, q = wiener_res
        m = pow(c, d, n)
        dec = decode_message(m)
        return format_result("Wiener Attack (Small Private Exponent d)", m, n, c, dec, {
            "p": str(p), "q": str(q), "d": str(d)
        })

    # Case 11: Small Prime Factorization (Trial division)
    small_p = None
    for p_cand in sympy.primerange(2, 2500000):
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
        return format_result(f"Trial Division (Faktor prima kecil: {p})", m, n, c, dec, {
            "p": str(p), "q": str(q), "d": str(d)
        })

    # Case 12: Pollard p-1
    pollard_res = solve_pollard_p1(n, B=100000)
    if pollard_res:
        p, q = pollard_res
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return format_result("Pollard's p-1 Factorization (p-1 smooth)", m, n, c, dec, {
            "p": str(p), "q": str(q), "d": str(d)
        })

    # Case 13: FactorDB Online
    fdb_res = solve_factordb(n)
    if fdb_res:
        p, q = fdb_res
        phi = (p - 1) * (q - 1)
        d = int(gmpy2.invert(e, phi))
        m = pow(c, d, n)
        dec = decode_message(m)
        return format_result("FactorDB Database Factorization", m, n, c, dec, {
            "p": str(p), "q": str(q), "d": str(d)
        })

    return {
        "success": False,
        "message": "Auto-detect mencoba Fermat, Wiener, Small e, Pollard p-1, Small Primes, dan FactorDB namun n tidak dapat difaktorkan secara instan. Coba gunakan tools eksternal (SageMath/Alpertron) di tab Referensi."
    }
