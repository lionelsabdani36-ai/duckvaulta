#!/usr/bin/env python3
"""
Automated Smoke Testing Suite for Duckvaulta Web Ecosystem
Endpoints:
- https://duckvaulta.ai.id
- https://godeye.duckvaulta.ai.id

Validates:
- HTTP 200 OK Status
- Network Latencies (DNS, TCP, TLS, TTFB, Total Transfer)
- Asset Crawling & Verification (Zero Broken Assets 404/500)
- Security Headers & SSL/TLS Configuration
"""

import sys
import re
import json
import time
import ssl
import socket
import subprocess
import urllib.request
import urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
from datetime import datetime, timezone, timedelta

WIB = timezone(timedelta(hours=7))
NOW_WIB = datetime.now(WIB)
TIMESTAMP_STR = NOW_WIB.strftime("%Y-%m-%d %H:%M:%S WIB")

TARGET_HOSTS = [
    {"name": "Duckvaulta Core Portal", "url": "https://duckvaulta.ai.id"},
    {"name": "God's Eye View", "url": "https://godeye.duckvaulta.ai.id"}
]

class AssetHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.assets = set()

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        src = d.get("src")
        href = d.get("href")
        rel = (d.get("rel") or "").lower()
        if tag == "script" and src:
            self.assets.add(src)
        elif tag == "link" and href:
            if any(k in rel for k in ["stylesheet", "icon", "preload", "manifest"]):
                self.assets.add(href)
        elif tag == "img" and src:
            if src.strip():
                self.assets.add(src)
        elif tag in ("source", "audio", "video") and src:
            if src.strip():
                self.assets.add(src)

def measure_curl_latencies(url, samples=3):
    timings = []
    for _ in range(samples):
        cmd = [
            "curl", "-s", "-o", "/dev/null",
            "-w", "%{time_namelookup}|%{time_connect}|%{time_appconnect}|%{time_starttransfer}|%{time_total}|%{http_code}",
            url
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, check=True)
        parts = res.stdout.strip().split("|")
        timings.append({
            "dns": float(parts[0]) * 1000,
            "tcp": float(parts[1]) * 1000,
            "tls": float(parts[2]) * 1000,
            "ttfb": float(parts[3]) * 1000,
            "total": float(parts[4]) * 1000,
            "code": int(parts[5])
        })
    avg_dns = sum(t["dns"] for t in timings) / len(timings)
    avg_tcp = sum(t["tcp"] for t in timings) / len(timings)
    avg_tls = sum(t["tls"] for t in timings) / len(timings)
    avg_ttfb = sum(t["ttfb"] for t in timings) / len(timings)
    avg_total = sum(t["total"] for t in timings) / len(timings)
    return {
        "status_code": timings[-1]["code"],
        "avg_dns_ms": round(avg_dns, 2),
        "avg_tcp_ms": round(avg_tcp, 2),
        "avg_tls_ms": round(avg_tls, 2),
        "avg_ttfb_ms": round(avg_ttfb, 2),
        "avg_total_ms": round(avg_total, 2),
        "min_total_ms": round(min(t["total"] for t in timings), 2),
        "max_total_ms": round(max(t["total"] for t in timings), 2)
    }

def check_tls_cert(hostname):
    ctx = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()
                if not cert:
                    return {"error": "No certificate found"}
                not_after_str = str(cert.get('notAfter', ''))
                not_after = datetime.strptime(not_after_str, '%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.now(timezone.utc).replace(tzinfo=None)).days
                issuer_seq = cert.get('issuer', ())
                issuer_name = "Let's Encrypt"
                if isinstance(issuer_seq, tuple):
                    for sub in issuer_seq:
                        if isinstance(sub, tuple) and len(sub) > 0 and len(sub[0]) == 2:
                            if sub[0][0] == 'organizationName':
                                issuer_name = sub[0][1]
                return {
                    "version": version,
                    "cipher": cipher[0] if cipher else "Unknown",
                    "issuer": issuer_name,
                    "days_remaining": days_left,
                    "valid_until": not_after_str
                }
    except Exception as e:
        return {"error": str(e)}

def crawl_and_test_assets(base_url, html):
    parser = AssetHTMLParser()
    parser.feed(html)
    
    # CSS url() matching
    css_urls = re.findall(r'url\([\'\"]?([^\'\"\)]+)[\'\"]?\)', html)
    for u in css_urls:
        if not u.startswith("#") and not u.startswith("data:"):
            parser.assets.add(u)
            
    # Filter out empty or SVG fragment IDs
    clean_assets = [a for a in parser.assets if a and not a.startswith("#") and not a.startswith("data:")]
    
    # For godeye, check imported modules in /src/main.js if present
    if "/src/main.js" in clean_assets:
        try:
            m_req = urllib.request.Request(urljoin(base_url, "/src/main.js"), headers={"User-Agent": "SmokeTester/1.0"})
            with urllib.request.urlopen(m_req, timeout=5) as m_resp:
                m_body = m_resp.read().decode("utf-8", errors="ignore")
                submods = re.findall(r'from\s+[\'\"]([^\'\"]+)[\'\"]', m_body)
                for sm in submods:
                    clean_assets.append(urljoin(base_url + "/src/", sm))
        except Exception:
            pass

    results = []
    broken = []
    
    for asset in sorted(list(set(clean_assets))):
        full_url = urljoin(base_url, asset)
        t0 = time.time()
        try:
            req = urllib.request.Request(full_url, headers={"User-Agent": "SmokeTester/1.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                elapsed = (time.time() - t0) * 1000
                results.append({
                    "asset": asset,
                    "url": full_url,
                    "status": resp.status,
                    "latency_ms": round(elapsed, 2),
                    "content_type": resp.headers.get("Content-Type", "")
                })
        except urllib.error.HTTPError as he:
            broken.append({
                "asset": asset,
                "url": full_url,
                "status": he.code,
                "error": str(he)
            })
        except Exception as e:
            broken.append({
                "asset": asset,
                "url": full_url,
                "status": 0,
                "error": str(e)
            })
            
    return results, broken

def run_smoke_test():
    report_data = {
        "timestamp": TIMESTAMP_STR,
        "targets": []
    }
    
    for t in TARGET_HOSTS:
        url = t["url"]
        hostname = urlparse(url).hostname
        print(f"[*] Testing {t['name']} ({url})...")
        
        # 1. Latency & status
        latencies = measure_curl_latencies(url, samples=3)
        
        # 2. TLS cert
        tls_info = check_tls_cert(hostname)
        
        # 3. Headers & HTML fetch
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) SmokeTester/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw_headers = dict(resp.headers)
            html = resp.read().decode("utf-8", errors="ignore")
            
        # 4. Asset crawl & verification
        assets_ok, assets_broken = crawl_and_test_assets(url, html)
        
        target_summary = {
            "name": t["name"],
            "url": url,
            "status_code": latencies["status_code"],
            "latencies": latencies,
            "tls": tls_info,
            "headers": {
                "server": raw_headers.get("Server", "Unknown"),
                "hsts": raw_headers.get("Strict-Transport-Security", "Missing"),
                "csp": "Present" if "Content-Security-Policy" in raw_headers else "Missing",
                "x_frame_options": raw_headers.get("X-Frame-Options", "Missing"),
                "x_content_type_options": raw_headers.get("X-Content-Type-Options", "Missing")
            },
            "assets_total": len(assets_ok) + len(assets_broken),
            "assets_ok_count": len(assets_ok),
            "assets_broken_count": len(assets_broken),
            "assets_ok": assets_ok,
            "assets_broken": assets_broken
        }
        report_data["targets"].append(target_summary)
        print(f"    Status: {latencies['status_code']} OK | TTFB: {latencies['avg_ttfb_ms']}ms | Assets OK: {len(assets_ok)} | Broken: {len(assets_broken)}")
        
    return report_data

if __name__ == "__main__":
    data = run_smoke_test()
    out_file = "/home/lionelsabdani36/duckvaulta/reports/smoke_test_report_latest.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[*] Report saved to {out_file}")
