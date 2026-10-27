#!/usr/bin/env python3
"""
SRE Health & Broken Asset Probe Script
Duckvaulta Production Ecosystem (Q4 2026)
Master Guru Judith & Tim AI Duckvaulta
"""

import sys
import time
import ssl
import json
import urllib.request
from urllib.parse import urljoin

TARGETS = [
    {
        "name": "Duckvaulta Portal",
        "url": "https://duckvaulta.ai.id/",
        "host": "duckvaulta.ai.id",
        "max_ttfb_ms": 50.0,
        "expected_status": 200,
        "critical_assets": [
            "/assets/anime.min.js",
            "/assets/duck-emblem.png",
            "/api/health.json",
            "/api/services.json",
            "/api/telemetry.json"
        ]
    },
    {
        "name": "Gods Eye View",
        "url": "https://godeye.duckvaulta.ai.id/",
        "host": "godeye.duckvaulta.ai.id",
        "max_ttfb_ms": 100.0,
        "expected_status": 200,
        "critical_assets": [
            "/@vite/client",
            "/cesium/Widgets/widgets.css",
            "/icons/icon-180.png",
            "/icons/icon-32.png",
            "/logo.svg",
            "/pin.svg",
            "/src/main.js",
            "/style.css"
        ]
    },
    {
        "name": "EdTech AI Platform",
        "url": "https://edtech.duckvaulta.ai.id/",
        "host": "edtech.duckvaulta.ai.id",
        "max_ttfb_ms": 50.0,
        "expected_status": 200,
        "critical_assets": []
    },
    {
        "name": "Ruang 3D Virtual Office",
        "url": "https://aicompany.duckvaulta.ai.id/",
        "host": "aicompany.duckvaulta.ai.id",
        "max_ttfb_ms": 60.0,
        "expected_status": 200,
        "critical_assets": []
    }
]

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def probe_url(url, host=None, timeout=5.0):
    ctx = create_ssl_context()
    headers = {"User-Agent": "SRE-Health-Probe/2026.1"}
    if host:
        headers["Host"] = host
    
    t0 = time.perf_counter()
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=timeout) as resp:
            data = resp.read()
            ttfb = (time.perf_counter() - t0) * 1000.0
            headers_dict = {k.lower(): v for k, v in resp.getheaders()}
            return {
                "status": resp.status,
                "ttfb_ms": round(ttfb, 2),
                "bytes": len(data),
                "headers": headers_dict,
                "error": None
            }
    except Exception as e:
        ttfb = (time.perf_counter() - t0) * 1000.0
        return {
            "status": getattr(e, "code", 0),
            "ttfb_ms": round(ttfb, 2),
            "bytes": 0,
            "headers": {},
            "error": str(e)
        }

def run_sre_audit():
    print("============================================================")
    print(" SRE Observability & Broken Asset Probe (Duckvaulta Q4 2026)")
    print("============================================================")
    all_passed = True
    total_assets = 0
    broken_assets = 0

    for target in TARGETS:
        name = target["name"]
        url = target["url"]
        host = target["host"]
        max_ttfb = target["max_ttfb_ms"]
        
        probe_res = probe_url(url, host=host)
        status = probe_res["status"]
        ttfb = probe_res["ttfb_ms"]
        headers = probe_res["headers"]
        
        status_ok = (status == target["expected_status"])
        latency_ok = (ttfb <= max_ttfb)
        hsts_ok = "strict-transport-security" in headers
        
        print("\nTarget: " + name + " (" + url + ")")
        print("  HTTP Status: " + str(status) + " [Expected: " + str(target['expected_status']) + "] -> " + ("PASS" if status_ok else "FAIL"))
        print("  TTFB Latency: " + str(ttfb) + " ms [SLA Limit: " + str(max_ttfb) + " ms] -> " + ("PASS" if latency_ok else "FAIL"))
        print("  HSTS Header: " + ("PRESENT" if hsts_ok else "MISSING") + " -> " + ("PASS" if hsts_ok else "WARN"))
        
        if not (status_ok and latency_ok):
            all_passed = False

        assets = target.get("critical_assets", [])
        for asset_path in assets:
            total_assets += 1
            asset_url = urljoin(url, asset_path)
            asset_res = probe_url(asset_url, host=host)
            a_status = asset_res["status"]
            a_ttfb = asset_res["ttfb_ms"]
            a_bytes = asset_res["bytes"]
            
            if a_status == 200 and a_bytes > 0:
                print("    [ASSET OK] " + asset_path + " (Status " + str(a_status) + ", " + str(a_bytes) + " bytes, " + str(a_ttfb) + " ms)")
            else:
                broken_assets += 1
                all_passed = False
                print("    [ASSET FAIL] " + asset_path + " (Status " + str(a_status) + ", Error: " + str(asset_res['error']) + ")")

    print("\n============================================================")
    print(" Ringkasan Audit SRE:")
    print(" Total Aset Diaudit : " + str(total_assets))
    print(" Broken Assets      : " + str(broken_assets))
    print(" Status Reliabilitas: " + ("100% HEALTHY" if all_passed else "DEGRADED"))
    print("============================================================")
    return 0 if all_passed else 1

if __name__ == '__main__':
    sys.exit(run_sre_audit())
