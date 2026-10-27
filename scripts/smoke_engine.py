#!/usr/bin/env python3
"""Automated smoke tests and internal asset discovery for Duckvaulta."""

from __future__ import annotations

import argparse
import hashlib
import http.client
import json
import math
import os
import socket
import ssl
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from time import perf_counter_ns
from typing import Any, Iterable
from urllib.parse import urljoin, urlsplit, urlunsplit


SCRIPT_VERSION = "1.0.0"
DEFAULT_TIMEOUT_SECONDS = 8.0
DEFAULT_MAX_DISCOVERED_ASSETS = 500
DEFAULT_CAPTURE_LIMIT_BYTES = 8 * 1024 * 1024
CHUNK_SIZE_BYTES = 64 * 1024
VALID_STATUS_CODES = [200, 301, 302, 307, 308]

PUBLIC_ENDPOINTS = [
    ("public_homepage", "https://duckvaulta.ai.id/"),
    ("public_health", "https://duckvaulta.ai.id/api/health.json"),
    ("public_services", "https://duckvaulta.ai.id/api/services.json"),
    ("public_telemetry", "https://duckvaulta.ai.id/api/telemetry.json"),
    ("public_aicompany", "https://aicompany.duckvaulta.ai.id/"),
    ("public_godeye", "https://godeye.duckvaulta.ai.id/"),
    ("public_edtech", "https://edtech.duckvaulta.ai.id/"),
    ("public_logo", "https://duckvaulta.ai.id/assets/logo.png"),
    ("public_duck_lockup", "https://duckvaulta.ai.id/assets/duck-lockup.png"),
    ("public_logo_transparent", "https://duckvaulta.ai.id/assets/logo-transparent.png"),
    ("public_anime", "https://duckvaulta.ai.id/assets/anime.min.js"),
    ("public_duck_emblem", "https://duckvaulta.ai.id/assets/duck-emblem.png"),
    (
        "public_client_side_challenge",
        "https://duckvaulta.ai.id/ctf-challenges/66-dont-use-client-side/index.html",
    ),
    (
        "public_perceptron_challenge",
        "https://duckvaulta.ai.id/ctf-challenges/779-perceptron/index.html",
    ),
    (
        "public_blame_game_archive",
        "https://duckvaulta.ai.id/ctf-challenges/405-blame-game.zip",
    ),
    ("public_drawio", "https://duckvaulta.ai.id/drawio/index.html"),
]

LOCAL_ENDPOINTS = [
    ("local_nginx", "http://127.0.0.1:80/"),
    ("local_ruang_3d", "http://127.0.0.1:3001/"),
    ("local_gods_eye", "http://127.0.0.1:4173/"),
    ("local_hermes_api", "http://127.0.0.1:20128/"),
    ("local_hermes_dashboard", "http://127.0.0.1:20128/dashboard"),
    ("local_discord_service", "http://127.0.0.1:3005/"),
]

SECURITY_HEADERS = [
    ("hsts", "Strict-Transport-Security"),
    ("csp", "Content-Security-Policy"),
    ("x_frame_options", "X-Frame-Options"),
    ("x_content_type_options", "X-Content-Type-Options"),
    ("referrer_policy", "Referrer-Policy"),
    ("cors", "Access-Control-Allow-Origin"),
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def elapsed_ms(start_ns: int, end_ns: int | None = None) -> float:
    end_ns = end_ns if end_ns is not None else perf_counter_ns()
    return round((end_ns - start_ns) / 1_000_000, 3)


def ascii_text(value: Any) -> str:
    """Return report-safe ASCII text and prevent table delimiters."""
    text = str(value).replace("\r", " ").replace("\n", " ").replace("|", "\\|")
    return text.encode("ascii", "replace").decode("ascii")


def header_map(message: Iterable[tuple[str, str]]) -> dict[str, str]:
    headers: dict[str, str] = {}
    for name, value in message:
        key = name.lower()
        safe_value = "<redacted>" if key == "set-cookie" else value.strip()
        if key in headers:
            headers[key] = f"{headers[key]}, {safe_value}"
        else:
            headers[key] = safe_value
    return headers


def security_audit(headers: dict[str, str]) -> dict[str, dict[str, Any]]:
    audit: dict[str, dict[str, Any]] = {}
    for key, header_name in SECURITY_HEADERS:
        value = headers.get(header_name.lower())
        audit[key] = {
            "header": header_name,
            "present": value is not None,
            "value": value,
        }
    return audit


def empty_timings() -> dict[str, float | None]:
    return {
        "dns_lookup_ms": None,
        "tcp_connect_ms": None,
        "tls_handshake_ms": None,
        "ttfb_ms": None,
        "download_ms": None,
        "total_latency_ms": None,
    }


def parse_target(url: str) -> tuple[str, str, int, str]:
    parsed = urlsplit(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"unsupported URL scheme: {parsed.scheme or '<none>'}")
    if not parsed.hostname:
        raise ValueError("URL has no hostname")
    default_port = 443 if parsed.scheme == "https" else 80
    port = parsed.port or default_port
    path = parsed.path or "/"
    if parsed.query:
        path = f"{path}?{parsed.query}"
    return parsed.scheme, parsed.hostname, port, path


def probe_url(
    url: str,
    role: str,
    source: str,
    timeout_seconds: float,
    capture_limit_bytes: int = 0,
) -> tuple[dict[str, Any], bytes]:
    """Probe one URL with a direct socket so each network phase is measurable."""
    started_ns = perf_counter_ns()
    record: dict[str, Any] = {
        "target": url,
        "role": role,
        "source": source,
        "roles": [role],
        "sources": [source],
        "started_at_utc": now_utc(),
        "scheme": None,
        "hostname": None,
        "port": None,
        "path": None,
        "status_code": None,
        "reason": None,
        "valid_status": False,
        "passed": False,
        "error": None,
        "resolved_addresses": [],
        "connect_attempts": [],
        "response_headers": {},
        "security_headers": security_audit({}),
        "body_bytes": 0,
        "sha256": None,
        "transfer_speed_kbps": None,
        "timings_ms": empty_timings(),
    }
    captured = bytearray()
    sock: socket.socket | ssl.SSLSocket | None = None
    response: http.client.HTTPResponse | None = None

    try:
        scheme, hostname, port, path = parse_target(url)
        record.update(
            {
                "scheme": scheme,
                "hostname": hostname,
                "port": port,
                "path": path,
            }
        )

        dns_start_ns = perf_counter_ns()
        address_info = socket.getaddrinfo(
            hostname,
            port,
            family=socket.AF_UNSPEC,
            type=socket.SOCK_STREAM,
        )
        record["timings_ms"]["dns_lookup_ms"] = elapsed_ms(dns_start_ns)
        unique_info: list[tuple[Any, ...]] = []
        seen_addresses: set[tuple[Any, ...]] = set()
        for info in address_info:
            address_key = (info[0], info[4])
            if address_key not in seen_addresses:
                seen_addresses.add(address_key)
                unique_info.append(info)
                record["resolved_addresses"].append(str(info[4][0]))

        connect_error_messages: list[str] = []
        for family, socktype, proto, _canonname, sockaddr in unique_info:
            candidate: socket.socket | None = None
            connect_start_ns = perf_counter_ns()
            try:
                candidate = socket.socket(family, socktype, proto)
                candidate.settimeout(timeout_seconds)
                candidate.connect(sockaddr)
                record["connect_attempts"].append(
                    {
                        "address": str(sockaddr),
                        "elapsed_ms": elapsed_ms(connect_start_ns),
                        "success": True,
                    }
                )
                record["timings_ms"]["tcp_connect_ms"] = elapsed_ms(connect_start_ns)
                sock = candidate
                break
            except OSError as exc:
                message = f"{type(exc).__name__}: {exc}"
                connect_error_messages.append(message)
                record["connect_attempts"].append(
                    {
                        "address": str(sockaddr),
                        "elapsed_ms": elapsed_ms(connect_start_ns),
                        "success": False,
                        "error": message,
                    }
                )
                if candidate is not None:
                    candidate.close()

        if sock is None:
            details = "; ".join(connect_error_messages) or "no address returned"
            raise OSError(f"TCP connect failed: {details}")

        if scheme == "https":
            tls_start_ns = perf_counter_ns()
            context = ssl.create_default_context()
            sock = context.wrap_socket(sock, server_hostname=hostname)
            record["timings_ms"]["tls_handshake_ms"] = elapsed_ms(tls_start_ns)

        host_header = hostname
        if (scheme == "http" and port != 80) or (scheme == "https" and port != 443):
            host_header = f"{hostname}:{port}"
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host_header}\r\n"
            "User-Agent: Duckvaulta-Smoke-Engine/1.0\r\n"
            "Accept: */*\r\n"
            "Accept-Encoding: identity\r\n"
            "Connection: close\r\n\r\n"
        ).encode("ascii")
        request_start_ns = perf_counter_ns()
        sock.sendall(request)
        response = http.client.HTTPResponse(sock, method="GET", url=path)
        response.begin()
        record["timings_ms"]["ttfb_ms"] = elapsed_ms(request_start_ns)
        record["status_code"] = response.status
        record["reason"] = response.reason
        record["valid_status"] = response.status in VALID_STATUS_CODES
        record["response_headers"] = header_map(response.getheaders())
        record["security_headers"] = security_audit(record["response_headers"])

        digest = hashlib.sha256()
        body_start_ns = perf_counter_ns()
        while True:
            chunk = response.read(CHUNK_SIZE_BYTES)
            if not chunk:
                break
            digest.update(chunk)
            record["body_bytes"] += len(chunk)
            if capture_limit_bytes and len(captured) < capture_limit_bytes:
                remaining = capture_limit_bytes - len(captured)
                captured.extend(chunk[:remaining])
        record["timings_ms"]["download_ms"] = elapsed_ms(body_start_ns)
        record["sha256"] = digest.hexdigest()
        download_seconds = max((perf_counter_ns() - body_start_ns) / 1_000_000_000, 1e-9)
        record["transfer_speed_kbps"] = round(
            record["body_bytes"] / 1024 / download_seconds, 3
        )
    except Exception as exc:  # A smoke run must retain failures and continue.
        record["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        if response is not None:
            try:
                response.close()
            except OSError:
                pass
        if sock is not None:
            try:
                sock.close()
            except OSError:
                pass
        record["timings_ms"]["total_latency_ms"] = elapsed_ms(started_ns)
        record["passed"] = bool(record["valid_status"] and record["error"] is None)

    return record, bytes(captured)


class ReferenceParser(HTMLParser):
    """Collect URL-bearing HTML attributes without requiring third-party HTML tools."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[str] = []

    def handle_starttag(self, _tag: str, attrs: list[tuple[str, str | None]]) -> None:
        for name, value in attrs:
            if value is None:
                continue
            lower_name = name.lower()
            if lower_name in ("href", "src"):
                self.references.append(value.strip())
            elif lower_name == "srcset":
                for candidate in value.split(","):
                    reference = candidate.strip().split()[0] if candidate.strip() else ""
                    if reference:
                        self.references.append(reference)


def local_homepage_bytes() -> bytes | None:
    path = Path("/var/www/duckvaulta/index.html")
    try:
        if path.is_file():
            return path.read_bytes()
    except OSError:
        return None
    return None


def discover_internal_urls(
    html_bytes: bytes,
    base_url: str,
    local_mode: bool,
    max_assets: int,
) -> list[str]:
    parser = ReferenceParser()
    parser.feed(html_bytes.decode("utf-8", errors="replace"))
    base = urlsplit(base_url)
    discovered: list[str] = []
    seen: set[str] = set()
    local_hostname = base.hostname or "127.0.0.1"

    for raw_reference in parser.references:
        if not raw_reference or raw_reference.startswith(("#", "data:", "javascript:", "mailto:")):
            continue
        absolute = urljoin(base_url, raw_reference)
        parsed = urlsplit(absolute)
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            continue
        if local_mode:
            if parsed.hostname.lower() not in (local_hostname.lower(), "duckvaulta.ai.id"):
                continue
            absolute = urlunsplit(
                (
                    base.scheme,
                    base.netloc,
                    parsed.path or "/",
                    parsed.query,
                    "",
                )
            )
        elif parsed.hostname.lower() != (base.hostname or "").lower():
            continue
        else:
            absolute = urlunsplit(
                (parsed.scheme, parsed.netloc, parsed.path or "/", parsed.query, "")
            )
        if absolute not in seen:
            seen.add(absolute)
            discovered.append(absolute)
            if len(discovered) >= max_assets:
                break
    return discovered


def merge_duplicate_metadata(record: dict[str, Any], role: str, source: str) -> None:
    if role not in record["roles"]:
        record["roles"].append(role)
    if source not in record["sources"]:
        record["sources"].append(source)


def add_probe(
    records: list[dict[str, Any]],
    by_url: dict[str, dict[str, Any]],
    url: str,
    role: str,
    source: str,
    timeout_seconds: float,
    capture_limit_bytes: int = 0,
) -> tuple[dict[str, Any], bytes, bool]:
    if url in by_url:
        record = by_url[url]
        merge_duplicate_metadata(record, role, source)
        return record, b"", False
    record, body = probe_url(
        url,
        role=role,
        source=source,
        timeout_seconds=timeout_seconds,
        capture_limit_bytes=capture_limit_bytes,
    )
    records.append(record)
    by_url[url] = record
    return record, body, True


def percentile(values: list[float], percentile_value: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile_value / 100
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return round(ordered[lower], 3)
    weight = position - lower
    result = ordered[lower] + (ordered[upper] - ordered[lower]) * weight
    return round(result, 3)


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    latencies = [
        record["timings_ms"]["total_latency_ms"]
        for record in records
        if record["timings_ms"]["total_latency_ms"] is not None
    ]
    passed = sum(1 for record in records if record["passed"])
    slowest = max(records, key=lambda item: item["timings_ms"]["total_latency_ms"] or -1, default=None)
    fastest = min(
        (record for record in records if record["timings_ms"]["total_latency_ms"] is not None),
        key=lambda item: item["timings_ms"]["total_latency_ms"],
        default=None,
    )
    return {
        "count_tested_targets": len(records),
        "passed_targets": passed,
        "failed_targets": len(records) - passed,
        "pass_rate_percent": round((passed / len(records)) * 100, 2) if records else 0.0,
        "latency_ms": {
            "p50": percentile(latencies, 50),
            "p95": percentile(latencies, 95),
            "p99": percentile(latencies, 99),
            "sample_count": len(latencies),
        },
        "slowest_endpoint": (
            {
                "target": slowest["target"],
                "total_latency_ms": slowest["timings_ms"]["total_latency_ms"],
            }
            if slowest is not None
            else None
        ),
        "fastest_endpoint": (
            {
                "target": fastest["target"],
                "total_latency_ms": fastest["timings_ms"]["total_latency_ms"],
            }
            if fastest is not None
            else None
        ),
    }


def report_cell(value: Any) -> str:
    if value is None:
        return "n/a"
    if isinstance(value, bool):
        return "yes" if value else "no"
    return ascii_text(value)


def build_report(telemetry: dict[str, Any]) -> str:
    summary = telemetry["summary"]
    records = telemetry["targets"]
    lines = [
        "# Duckvaulta Smoke Test Report",
        "",
        f"Generated: {ascii_text(telemetry['generated_at_utc'])}",
        f"Timeout per target: {report_cell(telemetry['configuration']['timeout_seconds'])} seconds",
        "",
        "## Summary",
        "",
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Targets tested | {summary['count_tested_targets']} |",
        f"| Passed | {summary['passed_targets']} |",
        f"| Failed | {summary['failed_targets']} |",
        f"| Pass rate | {summary['pass_rate_percent']}% |",
        f"| Latency p50 | {report_cell(summary['latency_ms']['p50'])} ms |",
        f"| Latency p95 | {report_cell(summary['latency_ms']['p95'])} ms |",
        f"| Latency p99 | {report_cell(summary['latency_ms']['p99'])} ms |",
        f"| Slowest | {report_cell(summary['slowest_endpoint']['target'] if summary['slowest_endpoint'] else None)} ({report_cell(summary['slowest_endpoint']['total_latency_ms'] if summary['slowest_endpoint'] else None)} ms) |",
        f"| Fastest | {report_cell(summary['fastest_endpoint']['target'] if summary['fastest_endpoint'] else None)} ({report_cell(summary['fastest_endpoint']['total_latency_ms'] if summary['fastest_endpoint'] else None)} ms) |",
        "",
        "## Target Results",
        "",
        "| Target | Status | Pass | DNS ms | TCP ms | TLS ms | TTFB ms | Total ms | Bytes | KB/s | SHA-256 |",
        "| --- | ---: | :---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for record in records:
        timings = record["timings_ms"]
        lines.append(
            "| "
            + " | ".join(
                [
                    report_cell(record["target"]),
                    report_cell(record["status_code"]),
                    report_cell(record["passed"]),
                    report_cell(timings["dns_lookup_ms"]),
                    report_cell(timings["tcp_connect_ms"]),
                    report_cell(timings["tls_handshake_ms"]),
                    report_cell(timings["ttfb_ms"]),
                    report_cell(timings["total_latency_ms"]),
                    report_cell(record["body_bytes"]),
                    report_cell(record["transfer_speed_kbps"]),
                    report_cell(record["sha256"]),
                ]
            )
            + " |"
        )

    lines.extend(
        [
            "",
            "## Security Header Audit",
            "",
            "Presence is checked from the response headers. A missing header is recorded as `no`.",
            "",
            "| Target | HSTS | CSP | X-Frame-Options | X-Content-Type-Options | Referrer-Policy | CORS |",
            "| --- | :---: | :---: | :---: | :---: | :---: | :---: |",
        ]
    )
    for record in records:
        audit = record["security_headers"]
        lines.append(
            "| "
            + " | ".join(
                [
                    report_cell(record["target"]),
                    report_cell(audit["hsts"]["present"]),
                    report_cell(audit["csp"]["present"]),
                    report_cell(audit["x_frame_options"]["present"]),
                    report_cell(audit["x_content_type_options"]["present"]),
                    report_cell(audit["referrer_policy"]["present"]),
                    report_cell(audit["cors"]["present"]),
                ]
            )
            + " |"
        )

    errors = [record for record in records if record["error"]]
    lines.extend(["", "## Errors", ""])
    if errors:
        lines.extend(["| Target | Error |", "| --- | --- |"])
        for record in errors:
            lines.append(f"| {report_cell(record['target'])} | {report_cell(record['error'])} |")
    else:
        lines.append("No probe errors.")

    lines.extend(
        [
            "",
            "## Crawl",
            "",
            f"Crawl source: {report_cell(telemetry['crawl']['source'])}",
            f"References discovered: {telemetry['crawl']['references_discovered']}",
            f"Unique discovered targets probed: {telemetry['crawl']['unique_targets_probed']}",
            "",
            "Telemetry file: `smoke_test_telemetry.json`",
            "",
        ]
    )
    return "\n".join(lines)


def run_engine(output_dir: Path, timeout_seconds: float, max_assets: int) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    by_url: dict[str, dict[str, Any]] = {}
    homepage_body = b""
    homepage_record: dict[str, Any] | None = None

    for role, url in PUBLIC_ENDPOINTS:
        capture_limit = DEFAULT_CAPTURE_LIMIT_BYTES if role == "public_homepage" else 0
        record, body, _created = add_probe(
            records,
            by_url,
            url,
            role,
            "required_public_endpoint",
            timeout_seconds,
            capture_limit,
        )
        if role == "public_homepage":
            homepage_record = record
            homepage_body = body

    crawl_source = "unavailable"
    crawl_base_url = "https://duckvaulta.ai.id/"
    local_mode = False
    if homepage_body:
        crawl_source = "remote_homepage"
    else:
        local_body = local_homepage_bytes()
        if local_body:
            homepage_body = local_body[:DEFAULT_CAPTURE_LIMIT_BYTES]
            crawl_source = "local_file:/var/www/duckvaulta/index.html"
            crawl_base_url = "http://127.0.0.1:80/"
            local_mode = True

    discovered_urls: list[str] = []
    if homepage_body:
        discovered_urls = discover_internal_urls(
            homepage_body,
            crawl_base_url,
            local_mode=local_mode,
            max_assets=max_assets,
        )
        for url in discovered_urls:
            add_probe(
                records,
                by_url,
                url,
                "discovered_internal_asset",
                crawl_source,
                timeout_seconds,
            )

    for role, url in LOCAL_ENDPOINTS:
        add_probe(
            records,
            by_url,
            url,
            role,
            "required_local_service",
            timeout_seconds,
        )

    ollama_api_url = "http://127.0.0.1:11434/api/version"
    ollama_api, _body, _created = add_probe(
        records,
        by_url,
        ollama_api_url,
        "local_ollama_api_version",
        "required_local_service",
        timeout_seconds,
    )
    if not ollama_api["passed"]:
        add_probe(
            records,
            by_url,
            "http://127.0.0.1:11434/",
            "local_ollama_root_fallback",
            "ollama_api_version_failed",
            timeout_seconds,
        )

    summary = aggregate(records)
    telemetry: dict[str, Any] = {
        "schema_version": "1.0",
        "engine_version": SCRIPT_VERSION,
        "generated_at_utc": now_utc(),
        "configuration": {
            "timeout_seconds": timeout_seconds,
            "valid_status_codes": VALID_STATUS_CODES,
            "max_discovered_assets": max_assets,
            "checksum": "SHA-256 over the complete response body",
        },
        "crawl": {
            "source": crawl_source,
            "base_url": crawl_base_url if crawl_source != "unavailable" else None,
            "references_discovered": len(discovered_urls),
            "unique_targets_probed": sum(1 for url in discovered_urls if url in by_url),
            "remote_homepage_status": homepage_record["status_code"] if homepage_record else None,
        },
        "summary": summary,
        "targets": records,
    }
    telemetry_path = output_dir / "smoke_test_telemetry.json"
    report_path = output_dir / "smoke_test_report.md"
    telemetry_path.write_text(json.dumps(telemetry, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    report_path.write_text(build_report(telemetry), encoding="ascii")

    print("Smoke test execution summary")
    print(f"Targets tested: {summary['count_tested_targets']}")
    print(f"Passed: {summary['passed_targets']}")
    print(f"Failed: {summary['failed_targets']}")
    print(f"Pass rate: {summary['pass_rate_percent']}%")
    print(f"Latency p50/p95/p99: {report_cell(summary['latency_ms']['p50'])}/{report_cell(summary['latency_ms']['p95'])}/{report_cell(summary['latency_ms']['p99'])} ms")
    slowest = summary["slowest_endpoint"]
    fastest = summary["fastest_endpoint"]
    print(f"Slowest endpoint: {report_cell(slowest['target'] if slowest else None)} ({report_cell(slowest['total_latency_ms'] if slowest else None)} ms)")
    print(f"Fastest endpoint: {report_cell(fastest['target'] if fastest else None)} ({report_cell(fastest['total_latency_ms'] if fastest else None)} ms)")
    print(f"Crawl source: {crawl_source}")
    print(f"References discovered: {len(discovered_urls)}")
    print(f"Telemetry: {telemetry_path}")
    print(f"Report: {report_path}")
    return telemetry


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe Duckvaulta endpoints and crawl internal homepage assets.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory for smoke_test_telemetry.json and smoke_test_report.md",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=float(os.environ.get("SMOKE_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)),
        help="Socket timeout for each target in seconds",
    )
    parser.add_argument(
        "--max-assets",
        type=int,
        default=DEFAULT_MAX_DISCOVERED_ASSETS,
        help="Maximum internal homepage references to probe",
    )
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be greater than zero")
    if args.max_assets < 0:
        parser.error("--max-assets must not be negative")
    try:
        run_engine(args.output_dir, args.timeout, args.max_assets)
    except OSError as exc:
        print(f"Smoke engine could not write output: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
