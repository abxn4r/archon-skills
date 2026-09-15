"""
Archon Terminal Dashboard
Zero-dependency ANSI colorized streaming dashboard & interactive TUI.
Visualizes active security debt, decision review dates, institutional memory metrics,
and installed coding agent integrations.
"""

import os
import sys
import time
from typing import Optional, Dict, Any

from archon.memory import stats, debt
from archon.detector import detect_installed_agents

# ANSI Colors & Formatting
ESC = "\033["
RESET = f"{ESC}0m"
BOLD = f"{ESC}1m"
DIM = f"{ESC}2m"
RED = f"{ESC}31m"
GREEN = f"{ESC}32m"
YELLOW = f"{ESC}33m"
BLUE = f"{ESC}34m"
MAGENTA = f"{ESC}35m"
CYAN = f"{ESC}36m"
WHITE = f"{ESC}37m"
BG_DARK = f"{ESC}48;5;235m"


def enable_windows_vt100() -> bool:
    """Enable VT100 terminal processing on Windows 10+ consoles."""
    if sys.platform != "win32":
        return True
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-11)  # STD_OUTPUT_HANDLE = -11
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        # ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        kernel32.SetConsoleMode(handle, mode.value | 0x0004)
        return True
    except Exception:
        return False


def render_dashboard_content(filter_advisor: Optional[str] = None) -> str:
    """Generate the complete dashboard text view."""
    st = stats()
    debts = debt(scope="all")
    agents = detect_installed_agents()

    lines = []
    width = 72

    # Top border
    lines.append(f"{CYAN}┌{'─' * (width - 2)}┐{RESET}")
    title = f"  ARCHON EXPERT ADVISOR SUITE & MEMORY DASHBOARD  "
    padding = (width - 2 - len(title)) // 2
    lines.append(f"{CYAN}│{RESET}{' ' * padding}{BOLD}{WHITE}{title}{RESET}{' ' * (width - 2 - len(title) - padding)}{CYAN}│{RESET}")
    lines.append(f"{CYAN}├{'─' * (width - 2)}┤{RESET}")

    # Metrics Summary Row
    total_recs = st["total_records"]
    local_count = st["scope_records"].get("local", 0)
    global_count = st["scope_records"].get("global", 0)
    sec_debts_count = len(debts)
    overdue_debts = sum(1 for d in debts if d["overdue"])

    metric_str = (
        f" Total Records: {BOLD}{total_recs}{RESET} | "
        f"Local (.archon): {BOLD}{local_count}{RESET} | "
        f"Global (~/.archon): {BOLD}{global_count}{RESET}"
    )
    lines.append(f"{CYAN}│{RESET} {metric_str:<{width - 4 + 18}} {CYAN}│{RESET}")
    lines.append(f"{CYAN}├{'─' * (width - 2)}┤{RESET}")

    # 1. Active Security Debt (Saltzer)
    lines.append(f"{CYAN}│{RESET} {BOLD}{RED}SALTZER SECURITY DEBT & RELEASE GATES{RESET}{' ' * (width - 38)}{CYAN}│{RESET}")
    if debts:
        for d in debts[:4]:
            sev = d["severity"]
            sev_col = RED if sev == "CRITICAL" else (YELLOW if sev == "HIGH" else GREEN)
            overdue_tag = f" {RED}[OVERDUE]{RESET}" if d["overdue"] else ""
            title_disp = d["title"][:38]
            owner = d["owner"][:10]
            line_txt = f"  * [{sev_col}{sev:<8}{RESET}] {title_disp} ({owner}){overdue_tag}"
            lines.append(f"{CYAN}│{RESET} {line_txt:<{width - 4 + 18}} {CYAN}│{RESET}")
    else:
        lines.append(f"{CYAN}│{RESET}   {GREEN}✓ No active security debt tracked across repositories.{RESET}{' ' * (width - 61)}{CYAN}│{RESET}")

    lines.append(f"{CYAN}├{'─' * (width - 2)}┤{RESET}")

    # 2. Decision Review Status (Seneca & Dijkstra)
    lines.append(f"{CYAN}│{RESET} {BOLD}{YELLOW}STRATEGIC & ARCHITECTURAL DECISIONS (SDR & MADR){RESET}{' ' * (width - 50)}{CYAN}│{RESET}")
    due_decisions = st["decisions"]["due"]
    upcoming_decisions = st["decisions"]["upcoming"]

    if due_decisions:
        for dec in due_decisions[:2]:
            lines.append(f"{CYAN}│{RESET}   {RED}! DUE FOR REVIEW{RESET}: {dec['review_date']} - {dec['decision'][:35]:<{width - 30}} {CYAN}│{RESET}")
    if upcoming_decisions:
        for dec in upcoming_decisions[:2]:
            lines.append(f"{CYAN}│{RESET}   {CYAN}- UPCOMING{RESET}      : {dec['review_date']} - {dec['decision'][:35]:<{width - 30}} {CYAN}│{RESET}")
    if not due_decisions and not upcoming_decisions:
        lines.append(f"{CYAN}│{RESET}   {DIM}No upcoming decisions scheduled for review.{RESET}{' ' * (width - 50)}{CYAN}│{RESET}")

    lines.append(f"{CYAN}├{'─' * (width - 2)}┤{RESET}")

    # 3. Advisor Activity Breakdown
    lines.append(f"{CYAN}│{RESET} {BOLD}{MAGENTA}ADVISOR ACTIVITY BREAKDOWN{RESET}{' ' * (width - 28)}{CYAN}│{RESET}")
    adv_parts = []
    for adv, cnt in sorted(st["advisors"].items()):
        adv_parts.append(f"{adv.capitalize()}: {cnt}")
    adv_str = " | ".join(adv_parts) if adv_parts else "No records logged yet."
    lines.append(f"{CYAN}│{RESET}   {adv_str:<{width - 5}} {CYAN}│{RESET}")

    lines.append(f"{CYAN}├{'─' * (width - 2)}┤{RESET}")

    # 4. Detected Coding Agents
    lines.append(f"{CYAN}│{RESET} {BOLD}{BLUE}DETECTED AI CODING AGENT INTEGRATIONS{RESET}{' ' * (width - 39)}{CYAN}│{RESET}")
    if agents:
        agent_names = [a["name"] for a in agents]
        agent_str = ", ".join(agent_names)
        lines.append(f"{CYAN}│{RESET}   {GREEN}✓ Detected:{RESET} {agent_str:<{width - 18}} {CYAN}│{RESET}")
    else:
        lines.append(f"{CYAN}│{RESET}   {DIM}None auto-detected; run 'archon export' for manual configs.{RESET}{' ' * (width - 66)}{CYAN}│{RESET}")

    # Bottom border
    lines.append(f"{CYAN}└{'─' * (width - 2)}┘{RESET}")
    lines.append(f"{DIM}Commands: [q] Quit  [r] Refresh  [1-6] Filter Advisor  [c] Council{RESET}")
    return "\n".join(lines)


def run_dashboard(interactive: Optional[bool] = None) -> None:
    """Run dashboard either as an interactive TUI or a single snapshot."""
    enable_windows_vt100()

    is_tty = sys.stdout.isatty() if interactive is None else interactive

    if not is_tty:
        # Non-interactive snapshot
        print(render_dashboard_content())
        return

    # Interactive event loop
    filter_adv = None
    try:
        while True:
            # Clear screen ANSI
            sys.stdout.write(f"{ESC}2J{ESC}H")
            sys.stdout.write(render_dashboard_content(filter_advisor=filter_adv))
            sys.stdout.flush()

            # Non-blocking input check
            ch = None
            if sys.platform == "win32":
                import msvcrt
                # Wait up to 1 second
                for _ in range(10):
                    if msvcrt.kbhit():
                        ch = msvcrt.getwch().lower()
                        break
                    time.sleep(0.1)
            else:
                import select
                rlist, _, _ = select.select([sys.stdin], [], [], 1.0)
                if rlist:
                    ch = sys.stdin.read(1).lower()

            if ch == "q":
                break
            elif ch == "r":
                continue
            elif ch == "1":
                filter_adv = "seneca"
            elif ch == "2":
                filter_adv = "dijkstra"
            elif ch == "3":
                filter_adv = "saltzer"
            elif ch == "4":
                filter_adv = "aperture"
            elif ch == "5":
                filter_adv = "caples"
            elif ch == "6":
                filter_adv = "orwell"
            elif ch == "0":
                filter_adv = None
    except KeyboardInterrupt:
        pass
    finally:
        print(f"\n{RESET}Dashboard closed.")
