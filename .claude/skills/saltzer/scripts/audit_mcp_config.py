#!/usr/bin/env python3
"""
Saltzer MCP Configuration Auditor
Zero-dependency Python standard library security auditor.

Audits Model Context Protocol (MCP) server configurations for:
- Shell & command injection risks
- Unpinned package execution (supply-chain)
- Over-privileged filesystem targets
- Plaintext secrets and API tokens in configs

Usage:
  python audit_mcp_config.py --file path/to/config.json
  python audit_mcp_config.py --test
"""

import sys
import json
import re
import argparse
from pathlib import Path
from typing import Dict, Any, List

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DANGEROUS_COMMANDS = {"cmd", "cmd.exe", "powershell", "powershell.exe", "pwsh", "bash", "sh", "zsh"}
SECRET_KEY_PATTERN = re.compile(r"(API[_-]?KEY|TOKEN|SECRET|PASSWORD|AUTH|CREDENTIAL)", re.I)
WILDCARD_PATH_PATTERN = re.compile(r"^(\*|[A-Za-z]:[\\/]?|/)$")


def audit_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
    findings = []
    if not isinstance(config_data, dict):
        return {"server_count": 0, "finding_count": 0, "findings": []}

    servers = config_data.get("mcpServers") or config_data.get("servers") or {}
    if not isinstance(servers, dict):
        servers = {}

    for s_name, s_conf in servers.items():
        if not isinstance(s_conf, dict):
            continue
        cmd = str(s_conf.get("command") or "")
        args = s_conf.get("args") or []
        if not isinstance(args, list):
            args = [args]
        env = s_conf.get("env") or {}
        if not isinstance(env, dict):
            env = {}

        # 1. Shell Command Risk
        cmd_base = Path(cmd).name.lower()
        if cmd_base in DANGEROUS_COMMANDS:
            findings.append({
                "server": s_name,
                "severity": "CRITICAL",
                "title": "Raw Shell Exposing Arbitrary Command Execution",
                "detail": f"Server '{s_name}' uses '{cmd}' directly. Any agent prompt injection can execute host commands.",
                "remediation": "Replace shell with targeted, standalone binary executable.",
            })

        # 2. Unpinned Package Execution (npx / uvx)
        if cmd_base in ("npx", "uvx"):
            has_version = any("@" in str(a) and not str(a).startswith("@") for a in args)
            has_pinned_flag = any(str(a) == "--exact" for a in args)
            if not has_version and not has_pinned_flag:
                findings.append({
                    "server": s_name,
                    "severity": "HIGH",
                    "title": "Unpinned Package Execution (Supply Chain Risk)",
                    "detail": f"Server '{s_name}' executes '{cmd} {' '.join(str(a) for a in args[:2])}' without version pin.",
                    "remediation": "Pin exact package version (e.g. package@1.2.3).",
                })

        # 3. Wildcard Filesystem Access
        for a in args:
            a_str = str(a).strip()
            if WILDCARD_PATH_PATTERN.match(a_str):
                findings.append({
                    "server": s_name,
                    "severity": "CRITICAL",
                    "title": "Over-privileged Filesystem Scope",
                    "detail": f"Server '{s_name}' targets root or wildcard directory: '{a_str}'.",
                    "remediation": "Restrict directory scope to specific project subdirectories.",
                })

        # 4. Plaintext Secrets in Config
        for k, v in env.items():
            if SECRET_KEY_PATTERN.search(str(k)) and v and not str(v).startswith("$"):
                findings.append({
                    "server": s_name,
                    "severity": "HIGH",
                    "title": "Plaintext Secret in Configuration",
                    "detail": f"Server '{s_name}' exposes secret key '{k}' in config file.",
                    "remediation": "Inject secret via environment variable at launch; do not commit in JSON.",
                })

    return {
        "server_count": len(servers),
        "finding_count": len(findings),
        "findings": findings,
    }


def print_report(res: Dict[str, Any]):
    print("=" * 70)
    print("              SALTZER MODEL CONTEXT PROTOCOL (MCP) AUDIT             ")
    print("=" * 70)
    print(f"Total Servers Audited : {res['server_count']}")
    print(f"Security Findings     : {res['finding_count']}")
    print()

    has_critical = any(f["severity"] == "CRITICAL" for f in res["findings"])

    if not res["findings"]:
        print("[PASS] All MCP servers comply with baseline security invariants.")
        print("[RELEASE GATE] VETO: NONE (Approved)")
        print("=" * 70)
        return

    for idx, f in enumerate(res["findings"], 1):
        sev_tag = f"[{f['severity']}]"
        print(f"{idx}. {sev_tag:<10} Server: {f['server']} -- {f['title']}")
        print(f"   Detail     : {f['detail']}")
        print(f"   Remediation: {f['remediation']}")
        print()

    print("=" * 70)
    if has_critical:
        print("[RELEASE VETO TRIGGERED]: CRITICAL FINDINGS PRESENT -- DO NOT SHIP.")
    else:
        print("[RELEASE GATE]: HIGH FINDINGS -- REQUIRES DOCUMENTED OWNER ACCEPTANCE.")
    print("=" * 70)


def run_self_test():
    print("[TEST] Running self-test on audit_mcp_config.py...")
    test_config = {
        "mcpServers": {
            "unsafe_shell": {
                "command": "bash",
                "args": ["-c", "echo test"],
            },
            "unpinned_npx": {
                "command": "npx",
                "args": ["-y", "some-unpinned-server"],
            },
            "wildcard_fs": {
                "command": "node",
                "args": ["server.js", "/"],
            },
            "plaintext_secret": {
                "command": "node",
                "args": ["server.js"],
                "env": {"DATABASE_PASSWORD": "supersecret123"},
            },
            "safe_server": {
                "command": "node",
                "args": ["server.js", "dist/workspace"],
                "env": {"API_KEY": "$MY_ENV_API_KEY"},
            },
        }
    }
    res = audit_config(test_config)
    if res["finding_count"] == 4 and res["server_count"] == 5:
        print("[TEST PASS] Successfully detected all 4 security vulnerability types.")
        return 0
    else:
        print(f"[TEST FAIL] Expected 4 findings, found {res['finding_count']}.")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="Saltzer MCP Configuration Security Auditor",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--file", help="Path to MCP JSON configuration file")
    parser.add_argument("--test", action="store_true", help="Run auditor test suite")

    args = parser.parse_args()

    if args.test:
        return run_self_test()

    if not args.file:
        # Default search paths
        candidates = [
            Path(".cursor/mcp.json"),
            Path(".vscode/mcp.json"),
            Path("mcp.json"),
            Path.home() / ".cursor" / "mcp.json",
        ]
        target_file = None
        for c in candidates:
            if c.exists():
                target_file = c
                break
        if not target_file:
            print("[INFO] No MCP configuration specified and none found at default locations.")
            print("Usage: python audit_mcp_config.py --file path/to/mcp.json")
            return 0
    else:
        target_file = Path(args.file).resolve()

    if not target_file.exists():
        print(f"[ERROR] Config file not found: {target_file}", file=sys.stderr)
        return 1

    try:
        with open(target_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON in {target_file}: {e}", file=sys.stderr)
        return 1

    res = audit_config(data)
    print_report(res)

    has_critical = any(f["severity"] == "CRITICAL" for f in res["findings"])
    return 1 if has_critical else 0


if __name__ == "__main__":
    sys.exit(main())
