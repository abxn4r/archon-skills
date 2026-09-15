"""
Archon Universal Command Line Interface
Main entrypoint for Archon Skill Suite & Compounding Institutional Memory Engine.
Zero external runtime dependencies.
"""

import sys
import json
import argparse
from pathlib import Path
from typing import Optional, List

from archon.paths import normalize_path, get_repo_root
from archon.memory import (
    record,
    learn,
    query,
    profile,
    stats,
    debt,
    init_scopes,
    estimate_tokens,
)
from archon.council import run_council
from archon.detector import detect_installed_agents
from archon.validator import validate_all_skills
from archon.dashboard import run_dashboard


def get_default_skills_dir() -> Path:
    """Locate canonical skills directory relative to this package or current repo."""
    cwd = Path.cwd()
    if (cwd / "skills").is_dir():
        return cwd / "skills"

    # Check parent of package
    pkg_root = Path(__file__).resolve().parent.parent
    if (pkg_root / "skills").is_dir():
        return pkg_root / "skills"

    return cwd / "skills"


def handle_init(args: argparse.Namespace) -> int:
    """Initialize Archon storage scopes and configure detected agents."""
    print("=" * 65)
    print("          ARCHON SYSTEM INITIALIZATION          ")
    print("=" * 65)

    created_scopes = init_scopes(scope=args.scope)
    for name, p in created_scopes.items():
        print(f"[+] Initialized {name.capitalize()} Scope : {p}")

    if not args.no_adapters:
        from adapters import run_export
        skills_dir = get_default_skills_dir()
        if skills_dir.exists():
            print("\n--- Auto-Configuring Installed AI Coding Agents ---")
            detected = detect_installed_agents()
            if detected:
                for agent in detected:
                    print(f"[+] Configuring {agent['name']} ({agent['target_desc']})...")
                    try:
                        run_export(
                            target=agent["adapter"],
                            skills_dir=skills_dir,
                            output_dir=Path.cwd(),
                        )
                    except Exception as e:
                        print(f"    [!] Warning: Failed to configure {agent['name']}: {e}")
                print("[+] Auto-configuration completed.")
            else:
                print("[i] No coding agents auto-detected. Use 'archon export --target all' to generate configs.")
        else:
            print(f"[!] Skills directory not found at {skills_dir}; skipped adapter export.")

    print("\n[+] Archon initialized successfully. Run 'archon dashboard' or 'archon --help'.")
    return 0


def handle_query(args: argparse.Namespace) -> int:
    """Query memory across scopes with optional token budgeting."""
    res = query(
        text=args.text,
        advisor=args.advisor,
        scope=args.scope,
        limit=args.limit,
        max_tokens=args.max_tokens,
        after_date=args.after,
        before_date=args.before,
    )

    if not res:
        if args.format == "json":
            print("[]")
        elif args.format == "tsv":
            pass
        else:
            print(f"No matches found for query '{args.text}'.")
        return 0

    if args.format == "json":
        items = [r["entry"] for r in res]
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return 0

    if args.format == "tsv":
        # Ultra-compact TSV for minimal LLM token consumption
        print("ID\tSCORE\tSCOPE\tADVISOR\tTYPE\tCONTENT")
        for r in res:
            e = r["entry"]
            d = e.get("data", {})
            content = (
                d.get("lesson")
                or d.get("decision")
                or d.get("title")
                or d.get("text")
                or d.get("content")
                or str(d)
            )
            content_clean = str(content).replace("\t", " ").replace("\n", " ")[:160]
            print(f"{e.get('id')}\t{r['score']}\t{r['scope']}\t{e.get('advisor')}\t{e.get('type')}\t{content_clean}")
        return 0

    # Default formatted table output
    total_est_tokens = sum(estimate_tokens(json.dumps(r["entry"])) for r in res)
    print(f"Found {len(res)} matches for '{args.text}' (Est. {total_est_tokens} tokens):\n")

    for i, r in enumerate(res, 1):
        e = r["entry"]
        adv = e.get("advisor", "global").upper()
        r_type = e.get("type", "record")
        eid = e.get("id", "-")
        score = r["score"]
        src = r["source"]
        scope_tag = r["scope"].upper()
        data_disp = e.get("data", {})

        if isinstance(data_disp, dict):
            content = (
                data_disp.get("lesson")
                or data_disp.get("decision")
                or data_disp.get("notes")
                or data_disp.get("title")
                or data_disp.get("text")
                or json.dumps(data_disp)
            )
        else:
            content = str(data_disp)

        if len(content) > 160:
            content = content[:157] + "..."

        print(f"[{i}] Score: {score} | ID: {eid} | Scope: [{scope_tag}] | Advisor: {adv} | Type: {r_type}")
        print(f"    Source : {src} (Line {r['line']})")
        print(f"    Tags   : {', '.join(e.get('tags', [])) or 'none'}")
        print(f"    Data   : {content}\n")

    return 0


def handle_record(args: argparse.Namespace) -> int:
    """Record a memory entry."""
    res = record(
        advisor=args.advisor,
        record_type=args.type,
        data=args.data,
        tags=args.tags,
        scope=args.scope,
    )
    print(f"[+] SUCCESS: Recorded {res['type']} [{res['id']}] for {res['advisor'].upper()}")
    print(f"    Scope       : {res.get('_scope')}")
    print(f"    Destination : {res.get('_target_file')}")
    return 0


def handle_learn(args: argparse.Namespace) -> int:
    """Log a validated lesson or insight."""
    res = learn(
        advisor=args.advisor,
        lesson=args.lesson,
        tags=args.tags,
        scope=args.scope,
    )
    print(f"[+] SUCCESS: Logged learning [{res['id']}] for {res['advisor'].upper()}")
    print(f"    Scope  : {res.get('_scope')}")
    print(f"    Lesson : {res['data'].get('lesson')}")
    return 0


def handle_profile(args: argparse.Namespace) -> int:
    """Display user cognitive profile."""
    content = profile(advisor=args.advisor)
    print(content)
    return 0


def handle_stats(args: argparse.Namespace) -> int:
    """Print institutional memory statistics."""
    st = stats()
    print("=" * 65)
    print("          ARCHON INSTITUTIONAL MEMORY METRICS          ")
    print("=" * 65)
    print(f"Total Records Across Scopes : {st['total_records']}")
    print("\n--- Scope Breakdown ---")
    for s_name, cnt in st["scope_records"].items():
        print(f"  * {s_name.capitalize():<12} : {cnt} records")
    print("\n--- By Specialist Advisor ---")
    for adv, cnt in sorted(st["advisors"].items()):
        print(f"  * {adv.upper():<12} : {cnt} records")
    print("\n--- Decision Reviews (SDR & MADR) ---")
    print(f"  * Total Decisions Recorded : {st['decisions']['total']}")
    print(f"  * Overdue for Review       : {st['decisions']['due_count']}")
    for d in st["decisions"]["due"]:
        print(f"    [!] OVERDUE: {d['review_date']} - {d['id']} ({d['decision']})")
    print(f"  * Upcoming Reviews         : {st['decisions']['upcoming_count']}")
    for d in st["decisions"]["upcoming"]:
        print(f"    [-] Next: {d['review_date']} - {d['id']} ({d['decision']})")
    print("\n--- Active Security Debt (Saltzer) ---")
    print(f"  * Total Active Debts : {st['security_debt']['total_active']}")
    print(f"  * Overdue Debts      : {st['security_debt']['overdue_count']}")
    print(f"  * Critical Severity  : {st['security_debt']['critical_count']}")
    print("\n--- Top Tags ---")
    if st["top_tags"]:
        for t, cnt in st["top_tags"]:
            print(f"  * {t:<20} : {cnt}")
    else:
        print("  (No tags recorded yet)")
    print("=" * 65)
    return 0


def handle_debt(args: argparse.Namespace) -> int:
    """Display tracked security debt from Saltzer."""
    debts = debt(scope=args.scope, include_resolved=args.all)
    print("=" * 70)
    print("            SALTZER SECURITY DEBT & RELEASE GATES            ")
    print("=" * 70)
    if not debts:
        print("[OK] No active security debt tracked across repositories.")
        return 0

    print(f"Total Active Security Debts: {len(debts)}\n")
    for d in debts:
        status = "[OVERDUE]" if d["overdue"] else "[ACTIVE]"
        resolved = " [RESOLVED]" if d["resolved"] else ""
        print(f"[{d['severity']}] {status}{resolved} {d['id']} | Scope: {d['scope'].upper()}")
        print(f"    Title  : {d['title']}")
        print(f"    Owner  : {d['owner']} | Expiry: {d['expiry'] or 'None'}")
        print(f"    Tags   : {', '.join(d['tags']) or 'none'}\n")
    return 0


def handle_council(args: argparse.Namespace) -> int:
    """Run Autonomous Consensus Council debate."""
    matrix = run_council(proposal=args.proposal, record_decision=not args.no_record)
    print(matrix)
    return 0


def handle_export(args: argparse.Namespace) -> int:
    """Export skills to target coding agent format."""
    from adapters import run_export
    skills_dir = normalize_path(args.skills) if args.skills else get_default_skills_dir()
    output_dir = normalize_path(args.output) if args.output else Path.cwd()

    if not skills_dir.exists():
        print(f"[!] Error: Skills directory does not exist at {skills_dir}", file=sys.stderr)
        return 1

    print(f"Exporting skills from {skills_dir} for target '{args.target}' to {output_dir}...")
    run_export(target=args.target, skills_dir=skills_dir, output_dir=output_dir)
    print("[+] Export completed successfully.")
    return 0


def handle_validate(args: argparse.Namespace) -> int:
    """Validate skills against agentskills.io standard and 500-line budget."""
    target_path = normalize_path(args.path) if args.path else get_default_skills_dir()
    print(f"Validating skills in {target_path}...\n")
    report = validate_all_skills(target_path)

    print("=" * 65)
    print("              SKILL SPECIFICATION & BUDGET REPORT              ")
    print("=" * 65)
    print(f"Total Skills Inspected : {report['total']}")
    print(f"Passing Skills         : {report['valid_count']}")
    print("")

    for s in report["skills"]:
        status = "[PASS]" if s["valid"] else "[FAIL]"
        print(f"{status} {s['name']:<16} ({s['line_count']} lines)")
        for err in s["errors"]:
            print(f"    [!] ERROR: {err}")
        for warn in s["warnings"]:
            print(f"    [-] WARN : {warn}")

    print("=" * 65)
    return 0 if report["all_passed"] else 1


def handle_detect(args: argparse.Namespace) -> int:
    """Inspect and list detected coding assistants on the machine."""
    detected = detect_installed_agents()
    print("=" * 65)
    print("          DETECTED AI CODING AGENTS & WORKSPACES          ")
    print("=" * 65)
    if not detected:
        print("[i] No coding agents auto-detected.")
        return 0

    print(f"Found {len(detected)} coding environment(s) on this machine:\n")
    for a in detected:
        print(f"[+] {a['name']}")
        print(f"    Target Config : {a['target_desc']}")
        for ev in a["evidence"]:
            print(f"    Evidence      : {ev}")
        print()
    print("Run 'archon init' to automatically configure these environments.")
    return 0


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        prog="archon",
        description="Archon: Universal Expert Skill Suite & Dual-Scope Memory Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init
    p_init = subparsers.add_parser("init", help="Initialize Archon scopes & auto-configure agents")
    p_init.add_argument("--scope", default="all", choices=["local", "global", "all"], help="Scope to initialize")
    p_init.add_argument("--no-adapters", action="store_true", help="Skip agent auto-configuration")

    # query
    p_query = subparsers.add_parser("query", help="Search memory with relevance & token ceiling")
    p_query.add_argument("text", help="Query search text (use '*' for wildcard)")
    p_query.add_argument("--advisor", default=None, help="Filter by advisor name")
    p_query.add_argument("--scope", default="all", choices=["local", "global", "all"], help="Scope filter")
    p_query.add_argument("--limit", type=int, default=10, help="Max results returned")
    p_query.add_argument("--max-tokens", type=int, default=None, help="Ceiling for token budget")
    p_query.add_argument("--format", default="table", choices=["table", "json", "tsv"], help="Output format")
    p_query.add_argument("--after", default=None, help="Filter records after date (YYYY-MM-DD)")
    p_query.add_argument("--before", default=None, help="Filter records before date (YYYY-MM-DD)")

    # record
    p_record = subparsers.add_parser("record", help="Record an entry into memory")
    p_record.add_argument("--advisor", required=True, help="Advisor name")
    p_record.add_argument("--type", required=True, help="Record type")
    p_record.add_argument("--data", required=True, help="JSON string or plain text content")
    p_record.add_argument("--tag", "--tags", dest="tags", default=None, help="Comma-separated tags")
    p_record.add_argument("--scope", default="auto", choices=["local", "global", "auto"], help="Storage scope")

    # learn
    p_learn = subparsers.add_parser("learn", help="Log a validated insight or preference")
    p_learn.add_argument("--advisor", required=True, help="Advisor logging the insight")
    p_learn.add_argument("--lesson", required=True, help="Lesson or observation text")
    p_learn.add_argument("--tag", "--tags", dest="tags", default=None, help="Comma-separated tags")
    p_learn.add_argument("--scope", default="auto", choices=["local", "global", "auto"], help="Storage scope")

    # profile
    p_profile = subparsers.add_parser("profile", help="Display founder cognitive model / profile")
    p_profile.add_argument("--advisor", default="seneca", help="Advisor profile (default: seneca)")

    # stats
    subparsers.add_parser("stats", help="Show memory metrics across scopes")

    # debt
    p_debt = subparsers.add_parser("debt", help="List tracked security debt entries")
    p_debt.add_argument("--scope", default="all", choices=["local", "global", "all"], help="Scope to inspect")
    p_debt.add_argument("--all", action="store_true", help="Include resolved items")

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Open ANSI terminal dashboard")
    p_dash.add_argument("--snapshot", action="store_true", help="Print single snapshot instead of interactive loop")

    # council
    p_council = subparsers.add_parser("council", help="Run Autonomous Consensus Council debate")
    p_council.add_argument("proposal", help="Proposal text to deliberate upon")
    p_council.add_argument("--no-record", action="store_true", help="Do not save debate to memory")

    # export
    p_export = subparsers.add_parser("export", help="Export skills to agent formats")
    p_export.add_argument(
        "--target",
        default="all",
        choices=["cursor", "claude_code", "windsurf", "copilot", "cline", "aider", "antigravity", "all"],
        help="Target agent format",
    )
    p_export.add_argument("--output", default=None, help="Destination directory (default: repo root)")
    p_export.add_argument("--skills", default=None, help="Source skills directory (default: ./skills)")

    # validate
    p_val = subparsers.add_parser("validate", help="Validate skills for agentskills.io compliance")
    p_val.add_argument("path", nargs="?", default=None, help="Path to skills directory (default: ./skills)")

    # detect
    subparsers.add_parser("detect", help="Auto-detect installed coding assistants")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    command_handlers = {
        "init": handle_init,
        "query": handle_query,
        "record": handle_record,
        "learn": handle_learn,
        "profile": handle_profile,
        "stats": handle_stats,
        "debt": handle_debt,
        "dashboard": lambda a: run_dashboard(interactive=not a.snapshot) or 0,
        "council": handle_council,
        "export": handle_export,
        "validate": handle_validate,
        "detect": handle_detect,
    }

    handler = command_handlers.get(args.command)
    if handler:
        try:
            return handler(args)
        except Exception as e:
            print(f"[!] Error executing '{args.command}': {e}", file=sys.stderr)
            return 1

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
