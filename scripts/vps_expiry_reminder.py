#!/usr/bin/env python3
"""
VPS Expiry Reminder Script for Hermes Cron Engine.
Monitors VPS billing cycle from /home/lionelsabdani36/.hermes/vps_billing.json
Outputs structured Discord alerts for direct delivery to user channel.
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone, timedelta

CONFIG_PATH = "/home/lionelsabdani36/.hermes/vps_billing.json"
DEFAULT_EXPIRY = "2026-11-14T15:00:00Z"
DEFAULT_START = "2026-10-14T15:04:30Z"

WIB = timezone(timedelta(hours=7))

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "hostname": "duckvaulta.ai.id",
        "ip_address": "34.135.45.195",
        "provider": "Google Cloud Platform (GCP)",
        "specs": "AMD EPYC 9B14 4 vCPU, 15GB RAM, 79GB NVMe",
        "provision_date": "2026-10-14",
        "expiry_date": "2026-11-14",
        "billing_cycle": "Monthly",
        "channel_id": "1561251399176814652",
        "warn_threshold_days": [10, 7, 5, 3, 2, 1, 0]
    }

def format_alert(days_left, hours_left, total_hours, expiry_dt_wib, cfg, is_critical):
    status_icon = "🚨" if is_critical else "⏳"
    header_color = "**CRITICAL ALERT**" if is_critical else "**MONITORING STATUS**"

    lines = [
        f"{status_icon} {header_color}: PENGINGAT MASA AKTIF VPS",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
        f"• **Sisa Waktu Aktif:** **{days_left} Hari {hours_left} Jam** ({total_hours:.1f} jam)",
        f"• **Jatuh Tempo (Expired):** {expiry_dt_wib.strftime('%d %B %Y pukul %H:%M WIB')}",
        f"• **Host Server:** `{cfg.get('hostname', 'duckvaulta.ai.id')}` ({cfg.get('ip_address', '34.135.45.195')})",
        f"• **Spesifikasi:** {cfg.get('specs', 'AMD EPYC 9B14 4 vCPU, 15GB RAM')}",
        f"• **Provider:** {cfg.get('provider', 'Google Cloud Platform (GCP)')}",
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    ]

    if is_critical:
        lines.extend([
            "⚠️ **TINDAKAN DIPERLUKAN SEGERA:**",
            "1. Lakukan pembayaran/perpanjangan sewa VPS di dashboard billing provider.",
            "2. Pastikan cadangan data (backup) sudah ter-sync ke repository GitHub:",
            "   `./duckvaulta/sync_and_commit.sh`",
            "3. Lakukan export snapshot database dan server Minecraft sebelum batas waktu berakhir."
        ])
    else:
        lines.extend([
            "ℹ️ **Catatan Sistem:**",
            "Pengingat otomatis dijadwalkan setiap hari pukul 09:00 WIB.",
            "Jika sudah diperpanjang, tanggal expiry dapat diperbarui di `~/.hermes/vps_billing.json`."
        ])

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="VPS Expiry Reminder")
    parser.add_argument("--test", action="store_true", help="Force output for testing")
    parser.add_argument("--force", action="store_true", help="Force output regardless of threshold")
    args = parser.parse_args()

    cfg = load_config()
    expiry_str = cfg.get("expiry_date", "2026-11-14")
    
    # Parse expiry string
    try:
        if "T" in expiry_str:
            expiry_dt = datetime.fromisoformat(expiry_str.replace("Z", "+00:00"))
        else:
            expiry_dt = datetime.strptime(expiry_str, "%Y-%m-%d").replace(tzinfo=timezone.utc, hour=15, minute=0)
    except Exception:
        expiry_dt = datetime(2026, 11, 14, 15, 0, tzinfo=timezone.utc)

    now_utc = datetime.now(timezone.utc)
    delta = expiry_dt - now_utc

    total_seconds = delta.total_seconds()
    total_hours = total_seconds / 3600.0
    days_left = int(total_seconds // 86400)
    hours_left = int((total_seconds % 86400) // 3600)

    expiry_dt_wib = expiry_dt.astimezone(WIB)
    thresholds = cfg.get("warn_threshold_days", [10, 7, 5, 3, 2, 1, 0])
    max_threshold = max(thresholds) if thresholds else 10

    is_critical = days_left <= 3

    # Output decision:
    # If test/force: always print
    # If scheduled cron: print only if days_left <= max_threshold (e.g. 10 days)
    if args.test or args.force or (days_left <= max_threshold):
        msg = format_alert(days_left, hours_left, total_hours, expiry_dt_wib, cfg, is_critical)
        print(msg)
    else:
        # Silent watchdog mode (still ample time left)
        sys.exit(0)

if __name__ == "__main__":
    main()
