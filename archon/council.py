"""
Archon Autonomous Consensus Council
Orchestrates multi-advisor debates on high-stakes proposals.
Synthesizes perspectives from Seneca, Dijkstra, Saltzer, Aperture, Caples, and Orwell,
producing a structured Consensus & Disagreements Matrix and a Strategic Decision Record.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from archon.memory import record


def analyze_proposal_perspectives(proposal: str) -> Dict[str, Dict[str, Any]]:
    """
    Generate deterministic expert assessments from each of the 6 specialist advisors.
    """
    p_lower = proposal.lower()

    # 1. Seneca (Strategy & Second Brain)
    is_type1 = any(w in p_lower for w in ("rewrite", "migrate", "vendor", "database", "license", "equity", "pricing"))
    seneca_verdict = {
        "advisor": "Seneca",
        "domain": "Strategy, Leverage & Reversibility",
        "door_type": "Type 1 (Irreversible / High Friction)" if is_type1 else "Type 2 (Reversible / Two-Way Door)",
        "leverage_assessment": (
            "High structural risk: Ensure this solves an existing bottleneck rather than serving as refinement-avoidance."
            if is_type1
            else "Low operational downside: Move quickly with high execution velocity."
        ),
        "pre_mortem_risk": "Cognitive displacement — building infrastructure in advance of proven customer demand.",
        "stance": "PROCEED WITH GUARDRAILS" if is_type1 else "EXECUTE IMMEDIATELY",
    }

    # 2. Dijkstra (Engineering Architect)
    is_complex = any(w in p_lower for w in ("microservice", "distributed", "nosql", "vector", "graphql", "kafka"))
    dijkstra_verdict = {
        "advisor": "Dijkstra",
        "domain": "Software Architecture & Simplicity",
        "simplicity_test": (
            "FAILS simplicity test until minimal solution is ruled out. Prefer boring, proven engineering."
            if is_complex
            else "PASSES simplicity test: minimal abstraction overhead."
        ),
        "operational_liability": (
            "Introduces multi-system failure modes and increases cognitive load across the team."
            if is_complex
            else "Contained within existing repository boundaries."
        ),
        "fitness_function": "Automated verification of contract boundaries & quote integrity.",
        "stance": "CHALLENGE COMPLEXITY" if is_complex else "APPROVE ARCHITECTURE",
    }

    # 3. Saltzer (Principal Security Engineer & Veto Gate)
    has_critical_veto = any(w in p_lower for w in ("raw shell tool", "eval(", "root access", "bypass auth", "plaintext secret", "disable auth"))
    has_security_risk = has_critical_veto or any(w in p_lower for w in ("auth", "token", "secret", "mcp", "public", "credential"))
    
    if has_critical_veto:
        veto_verdict = "RELEASE VETO (CRITICAL: DO NOT SHIP)"
        veto_blocked = True
        stance = "VETO"
    elif has_security_risk:
        veto_verdict = "CONDITIONAL APPROVAL (Requires Security Checklist)"
        veto_blocked = False
        stance = "AUDIT BOUNDARIES"
    else:
        veto_verdict = "APPROVED (No Veto Triggered)"
        veto_blocked = False
        stance = "APPROVE"

    saltzer_verdict = {
        "advisor": "Saltzer",
        "domain": "Security, Trust Boundaries & Attack Surfaces",
        "attack_surface_delta": "EXPANDED ATTACK SURFACE: Requires boundary validation." if has_security_risk else "NEUTRAL / BOUNDED ATTACK SURFACE",
        "trust_boundaries": "Verify least privilege on filesystem, process tokens, and external network calls.",
        "veto_verdict": veto_verdict,
        "veto_blocked": veto_blocked,
        "stance": stance,
    }

    # 4. Aperture (Design & UX Director)
    aperture_verdict = {
        "advisor": "Aperture",
        "domain": "Interface, Ergonomics & Cognitive Load",
        "ergonomic_impact": "Assess whether this adds mental friction or configuration overhead for the end user.",
        "craft_standard": "Linear/Stripe standard: Ensure feedback latency is <200ms and failure states are self-explanatory.",
        "stance": "OPTIMIZE ERGONOMICS",
    }

    # 5. Caples (Copy & Messaging Director)
    caples_verdict = {
        "advisor": "Caples",
        "domain": "Clarity, Value Proposition & Positioning",
        "clarity_test": "Can the benefit of this change be stated in one sentence without corporate buzzwords?",
        "positioning_alignment": "Align with unique differentiators (e.g. zero external dependencies, verifiable proofs).",
        "stance": "DEMAND CLARITY",
    }

    # 6. Orwell (Growth & Developer Reputation)
    orwell_verdict = {
        "advisor": "Orwell",
        "domain": "Developer Community, Open Source & Reputation",
        "reputation_impact": "Engineers respect boring technology that works reliably over flashy abstractions that break.",
        "narrative_angle": "Contrarian engineering post-mortem or blueprint case study for developer community.",
        "stance": "STRENGTHEN REPUTATION",
    }

    return {
        "seneca": seneca_verdict,
        "dijkstra": dijkstra_verdict,
        "saltzer": saltzer_verdict,
        "aperture": aperture_verdict,
        "caples": caples_verdict,
        "orwell": orwell_verdict,
    }


def synthesize_council_matrix(
    proposal: str,
    perspectives: Dict[str, Dict[str, Any]],
) -> str:
    """
    Format the complete multi-advisor debate and Consensus Matrix into markdown.
    """
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    lines.append("# ARCHON EXECUTIVE BOARD CONSENSUS COUNCIL")
    lines.append(f"**Proposal**: *\"{proposal}\"*")
    lines.append(f"**Convened**: {timestamp}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. ADVISOR PERSPECTIVES & INDEPENDENT INQUESTS")
    lines.append("")

    for adv_key in ["seneca", "dijkstra", "saltzer", "aperture", "caples", "orwell"]:
        adv = perspectives[adv_key]
        lines.append(f"### {adv['advisor'].upper()} ({adv['domain']})")
        lines.append(f"- **Stance**: `{adv['stance']}`")
        for k, v in adv.items():
            if k not in ("advisor", "domain", "stance"):
                key_clean = k.replace("_", " ").title()
                lines.append(f"- **{key_clean}**: {v}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 2. CONSENSUS & DISAGREEMENTS MATRIX")
    lines.append("")
    lines.append("| Advisor | Primary Imperative | Identified Risk | Recommendation |")
    lines.append("|---|---|---|---|")
    lines.append(f"| **Seneca** | Strategic leverage | Cognitive displacement & distraction | {perspectives['seneca']['door_type']} |")
    lines.append(f"| **Dijkstra** | Minimal complexity | Operational debt & maintenance burden | {perspectives['dijkstra']['simplicity_test']} |")
    lines.append(f"| **Saltzer** | Release security veto | Unvalidated trust boundaries | {perspectives['saltzer']['veto_verdict']} |")
    lines.append(f"| **Aperture** | Ergonomics & craft | Unnecessary developer friction | Maintain <200ms latency & clarity |")
    lines.append(f"| **Caples** | Communication clarity | Vague buzzwords & abstract promises | Prove value with empirical metrics |")
    lines.append(f"| **Orwell** | Compounding reputation | Algorithmic drift & hype decay | Ground decisions in open-source credibility |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. COUNCIL VERDICT & NEXT MILESTONE")
    lines.append("")

    veto_blocked = perspectives["saltzer"].get("veto_blocked", False)
    if veto_blocked:
        verdict = "**VETOED BY SALTZER**: Proposal introduces unmitigated critical security risk. Do NOT proceed."
    else:
        verdict = "**PROCEED WITH CONDITIONS**: Proposal approved subject to simplicity validation and security boundary checks."

    lines.append(f"**Final Board Ruling**: {verdict}")
    lines.append("")
    lines.append("### Prescribed Invariants:")
    lines.append("1. **Simplicity First**: Implement the smallest reversible slice before committing to a permanent architectural shift.")
    lines.append("2. **Empirical Gate**: Execute standard verification scripts (`verify_evidence_quotes.py`, `audit_mcp_config.py`) before shipping.")
    lines.append("3. **Institutional Record**: Log the resulting MADR into `.archon/dijkstra/reviews.jsonl`.")
    lines.append("")

    return "\n".join(lines)


def run_council(proposal: str, record_decision: bool = True) -> str:
    """
    Run an autonomous Council deliberation on a given proposal and optionally record it.
    """
    perspectives = analyze_proposal_perspectives(proposal)
    matrix = synthesize_council_matrix(proposal, perspectives)

    if record_decision:
        try:
            record(
                advisor="council",
                record_type="decision",
                data={
                    "proposal": proposal,
                    "summary": matrix[:500] + "...",
                    "perspectives": {k: v["stance"] for k, v in perspectives.items()},
                },
                tags=["council", "debate", "consensus"],
            )
        except Exception:
            pass

    return matrix
