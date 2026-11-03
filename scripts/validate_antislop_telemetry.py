#!/usr/bin/env python3
"""
Validation Script: Anti-Slop Guidelines & Cyber Status Telemetry
Checks Zero Em-Dash compliance, JSON schema, YAML syntax, and line length constraints.
Author: Judith (Master Guru & Mentor Akademik / Kompetisi)
"""

import json
import os
import re
import sys
import yaml

TARGET_FILES = [
    "/home/lionelsabdani36/duckvaulta/reports/judith_visual_antislop_guidelines_cyber_telemetry.md",
    "/home/lionelsabdani36/duckvaulta/reports/cyber_status_telemetry_matrix.json",
    "/home/lionelsabdani36/duckvaulta/apps/minecraft/config/tab_scoreboard_antislop.yml"
]

def check_zero_em_dash(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check for unicode em-dash, en-dash, or suspicious double hyphens
    em_dash_matches = re.findall(r"[\u2014\u2013]|(?<!-)(?<!\w)--(?!-)(?!\w)", content)
    return len(em_dash_matches), em_dash_matches

def strip_mc_color_codes(text):
    # Remove &a, &b, &1-9, &l, &m, etc., and hex formats <#RRGGBB>
    cleaned = re.sub(r"&[0-9a-fk-or]", "", text, flags=re.IGNORECASE)
    cleaned = re.sub(r"<#[0-9a-fA-F]{6}>|</#[0-9a-fA-F]{6}>", "", cleaned)
    return cleaned

def validate_json_matrix(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    assert "specification_version" in data, "Missing specification_version"
    assert "team_collaboration" in data, "Missing team_collaboration"
    assert "telemetry_metrics_matrix" in data, "Missing telemetry_metrics_matrix"
    assert len(data["telemetry_metrics_matrix"]) >= 5, "Insufficient telemetry metrics"
    return len(data["telemetry_metrics_matrix"])

def validate_yaml_config(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    
    assert "scoreboard" in config, "Missing scoreboard section"
    assert "header-footer" in config, "Missing header-footer section"
    
    sb = config["scoreboard"]
    assert sb.get("enabled") is True, "Scoreboard must be enabled"
    
    lines = sb["scoreboards"]["cyber-hub"]["lines"]
    violations = []
    
    for i, line in enumerate(lines):
        clean_text = strip_mc_color_codes(line)
        if len(clean_text) > 30:
            violations.append((i, line, len(clean_text)))
            
    return len(lines), violations

def main():
    print("=" * 65)
    print("CYCRAFT SMP: ANTI-SLOP & TELEMETRY COMPLIANCE AUDIT")
    print("Inspector: Judith (Master Guru & Mentor Akademik / Kompetisi)")
    print("=" * 65)
    
    total_errors = 0
    
    # 1. Zero Em-Dash Check
    print("\n[Phase 1] Zero Em-Dash Enforcement Audit:")
    for path in TARGET_FILES:
        rel_name = os.path.basename(path)
        if not os.path.exists(path):
            print(f"  [FAIL] File missing: {path}")
            total_errors += 1
            continue
        count, _ = check_zero_em_dash(path)
        if count == 0:
            print(f"  [PASS] {rel_name}: 0 em-dash violations detected.")
        else:
            print(f"  [FAIL] {rel_name}: {count} em-dash violations detected!")
            total_errors += count
            
    # 2. JSON Specification Validation
    print("\n[Phase 2] Telemetry Matrix JSON Validation:")
    json_path = TARGET_FILES[1]
    try:
        metric_count = validate_json_matrix(json_path)
        print(f"  [PASS] Schema integrity confirmed with {metric_count} defined metrics.")
    except Exception as e:
        print(f"  [FAIL] JSON validation failed: {str(e)}")
        total_errors += 1
        
    # 3. YAML Configuration Validation
    print("\n[Phase 3] TAB Configuration & Line Length Audit:")
    yaml_path = TARGET_FILES[2]
    try:
        line_count, line_violations = validate_yaml_config(yaml_path)
        if not line_violations:
            print(f"  [PASS] Scoreboard config valid ({line_count} lines, all within 30-char limit).")
        else:
            print(f"  [FAIL] Line length exceeded on {len(line_violations)} lines:")
            for idx, raw, length in line_violations:
                print(f"         Line {idx}: '{raw}' ({length} chars)")
            total_errors += len(line_violations)
    except Exception as e:
        print(f"  [FAIL] YAML validation failed: {str(e)}")
        total_errors += 1
        
    print("\n" + "=" * 65)
    if total_errors == 0:
        print("AUDIT VERDICT: 100% COMPLIANT WITH JUDITH ANTI-SLOP STANDARDS")
        print("Observability Signal-to-Noise Ratio: OPTIMAL (Zero-Slop Certified)")
        print("=" * 65)
        sys.exit(0)
    else:
        print(f"AUDIT VERDICT: FAILED WITH {total_errors} VIOLATIONS")
        print("=" * 65)
        sys.exit(1)

if __name__ == "__main__":
    main()
