#!/usr/bin/env python3
"""
Spade Agent Bridge (Cue by Manus)
Dispatcher CLI for orchestrating tasks to spade963@bot.cue.im.
Complies with Duckvaulta security sanitization and telemetry tracking.
"""

import argparse
import datetime
import json
import os
import re
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from urllib.parse import quote

SPADE_EMAIL = "spade963@bot.cue.im"
REPORTS_DIR = "/home/lionelsabdani36/duckvaulta/reports"
TASKS_FILE = os.path.join(REPORTS_DIR, "spade_tasks.json")

# Sensitive data sanitization patterns
SENSITIVE_PATTERNS = [
    (r'(?i)(api[_-]?key|secret|token|password|auth|bearer)\s*[:=]\s*["\']?([a-zA-Z0-9_\-\.]{12,})["\']?', r'\1: [REDACTED]'),
    (r'34\.135\.45\.195', 'vps.duckvaulta.internal'),
    (r'/home/lionelsabdani36', '~'),
    (r'(?i)AIzaSy[a-zA-Z0-9_\-]{33}', '[REDACTED_GOOGLE_KEY]'),
    (r'(?i)sk-[a-zA-Z0-9]{20,}', '[REDACTED_API_KEY]'),
]

def sanitize_text(text: str) -> str:
    """Scrub internal credentials, private IPs, and paths before sending."""
    sanitized = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        sanitized = re.sub(pattern, replacement, sanitized)
    return sanitized

def load_tasks() -> list:
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def save_task(task_entry: dict):
    os.makedirs(REPORTS_DIR, exist_ok=True)
    tasks = load_tasks()
    tasks.insert(0, task_entry)
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks[:100], f, indent=2)

def build_payload(goal: str, context: str = "", constraints: str = "", expected_format: str = "") -> str:
    body_lines = [
        "### Task Objective",
        goal.strip(),
        "",
    ]
    if context:
        body_lines.extend([
            "### Context & Background",
            context.strip(),
            "",
        ])
    if constraints:
        body_lines.extend([
            "### Operating Constraints",
            constraints.strip(),
            "",
        ])
    if expected_format:
        body_lines.extend([
            "### Required Deliverable Format",
            expected_format.strip(),
            "",
        ])
    body_lines.extend([
        "---",
        "Dispatched by David (Leader, Duckvaulta AI Operations)",
        "Reply directly to this email to report task execution output."
    ])
    return "\n".join(body_lines)

def send_via_smtp(subject: str, body: str) -> bool:
    smtp_host = os.environ.get("CUE_SMTP_HOST") or os.environ.get("EMAIL_SMTP_HOST")
    smtp_port = int(os.environ.get("CUE_SMTP_PORT") or os.environ.get("EMAIL_SMTP_PORT", 587))
    smtp_user = os.environ.get("CUE_SMTP_USER") or os.environ.get("EMAIL_ADDRESS")
    smtp_pass = os.environ.get("CUE_SMTP_PASS") or os.environ.get("EMAIL_PASSWORD")

    if not (smtp_host and smtp_user and smtp_pass):
        return False

    msg = MIMEMultipart()
    msg["From"] = smtp_user
    msg["To"] = SPADE_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"[!] SMTP Error: {e}", file=sys.stderr)
        return False

def dispatch_task(subject: str, goal: str, context: str = "", constraints: str = "", expected_format: str = "", task_type: str = "GENERAL"):
    subject_clean = sanitize_text(subject)
    raw_body = build_payload(goal, context, constraints, expected_format)
    sanitized_body = sanitize_text(raw_body)
    ticket_id = f"TICK-{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d%H%M%S')}"

    print("==================================================")
    print(f"DISPATCHING TASK TO SPADE ({SPADE_EMAIL})")
    print(f"Type      : {task_type}")
    print(f"Ticket ID : {ticket_id}")
    print(f"Subject   : {subject_clean}")
    print("==================================================")
    
    sent = send_via_smtp(subject_clean, sanitized_body)
    
    task_record = {
        "ticket_id": ticket_id,
        "type": task_type,
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "recipient": SPADE_EMAIL,
        "subject": subject_clean,
        "body_preview": sanitized_body[:200] + ("..." if len(sanitized_body) > 200 else ""),
        "sent_via_smtp": sent,
        "status": "DISPATCHED" if sent else "PENDING_MANUAL_DELIVERY"
    }
    save_task(task_record)

    if sent:
        print("[+] SUCCESS: Dispatched directly to Spade via SMTP.")
    else:
        print("[*] Direct SMTP relay not configured. Pre-formatted delivery packet ready:\n")
        print("--- SUBJECT ---")
        print(subject_clean)
        print("\n--- BODY ---")
        print(sanitized_body)
        print("\n--- 1-CLICK MAILTO LINK ---")
        mailto_link = f"mailto:{SPADE_EMAIL}?subject={quote(subject_clean)}&body={quote(sanitized_body)}"
        print(mailto_link)
        print("\n[i] Ticket logged to reports/spade_tasks.json")

def cmd_send(args):
    dispatch_task(args.subject, args.goal, args.context, args.constraints, args.format, "GENERAL")

def cmd_architect(args):
    subject = f"[MINECRAFT ARCHITECT] Blueprint Request: {args.project}"
    goal = f"Design and produce a complete Minecraft 1.21 voxel architectural blueprint for: {args.project}."
    context = (
        f"Server World: cyber_skyblock (Void Skyblock Environment)\n"
        f"Target Coordinates: {args.location}\n"
        f"Dimensions / Footprint: {args.size}\n"
        f"Aesthetic Theme: {args.style}\n"
        f"Recommended Block Palette: Cyan stained glass, polished deepslate, sea lanterns, copper bulbs, smooth quartz, chiseled books."
    )
    constraints = (
        "1. Minecraft version: Purpur 1.21.4 native blocks.\n"
        "2. Do not use destructive or illegal blocks (no bedrock, barrier, command blocks, moving pistons).\n"
        "3. Enclose all vertical shafts and drop zones to prevent players falling into the void.\n"
        "4. Include interactive aesthetic elements (lighting switches, stairs, workstations)."
    )
    expected_format = (
        "Output:\n"
        "1. Concept summary and architectural lore.\n"
        "2. Voxel layer breakdown.\n"
        "3. Concrete Minecraft /fill and /setblock commands or a Python generator script producing .mcfunction files."
    )
    dispatch_task(subject, goal, context, constraints, expected_format, "ARCHITECT_BLUEPRINT")

def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("No task dispatches logged yet.")
        return
    print(f"Logged Spade Tasks ({len(tasks)} entries):")
    for t in tasks[:args.limit]:
        status_badge = "[SENT]" if t.get("sent_via_smtp") else "[PENDING]"
        ttype = t.get("type", "GEN")
        print(f" {status_badge} [{ttype}] {t.get('ticket_id')} | {t.get('timestamp')[:19]} | {t.get('subject')}")

def main():
    parser = argparse.ArgumentParser(description="Spade Agent Bridge (Cue by Manus)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # General send
    send_p = subparsers.add_parser("send", help="Dispatch a task to Spade")
    send_p.add_argument("--subject", "-s", required=True, help="Task title / subject line")
    send_p.add_argument("--goal", "-g", required=True, help="Task goal / main prompt")
    send_p.add_argument("--context", "-c", default="", help="Optional background context")
    send_p.add_argument("--constraints", default="", help="Operating constraints")
    send_p.add_argument("--format", default="", help="Required deliverable format")
    send_p.set_defaults(func=cmd_send)

    # Architect blueprint dispatch
    arch_p = subparsers.add_parser("architect", help="Request a Minecraft architectural blueprint from Spade")
    arch_p.add_argument("--project", "-p", required=True, help="Project name (e.g. 'Neo-Shibuya Skyport')")
    arch_p.add_argument("--location", "-l", default="cyber_skyblock (X=0, Y=105, Z=0)", help="Target build coordinates")
    arch_p.add_argument("--size", "-s", default="40x40x50", help="Footprint bounds (e.g. 40x40x50)")
    arch_p.add_argument("--style", default="Cyberpunk Brutalist Neon", help="Architectural aesthetic style")
    arch_p.set_defaults(func=cmd_architect)

    # List tasks
    list_p = subparsers.add_parser("list", help="List recent task dispatches")
    list_p.add_argument("--limit", "-n", type=int, default=10, help="Max records to show")
    list_p.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
