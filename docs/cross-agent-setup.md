# Universal Cross-Agent Setup & Adapters

Archon is designed to be agent-agnostic. Canonical skills are maintained under the open `agentskills.io` specification in `skills/` and can be exported instantly to any major AI coding assistant.

---

## 1. Supported AI Coding Agents

```
┌─────────────────┬───────────────────────────────────┬────────────────────────────────┐
│ Agent           │ Export Target Path                │ Primary Mechanism              │
├─────────────────┼───────────────────────────────────┼────────────────────────────────┤
│ Cursor          │ .cursor/rules/*.mdc               │ alwaysApply: false with globs  │
│ Claude Code     │ .claude/skills/ & .claude-plugin/ │ Native skill manifests         │
│ Windsurf        │ .windsurfrules & workflows/       │ Cascade rule routing           │
│ GitHub Copilot  │ .github/copilot-instructions.md   │ Compact prompt (<400 tokens)   │
│ Cline / Roo Code│ .clinerules & .roomodes           │ Custom persona modes & rules   │
│ Aider           │ CONVENTIONS.md & .aider.conf.yml  │ Standard conventions config    │
│ Antigravity     │ .agents/skills/                   │ Native Antigravity skills      │
└─────────────────┴───────────────────────────────────┴────────────────────────────────┘
```

---

## 2. One-Command Automatic Setup

Archon includes an intelligent auto-detector that scans your environment for installed coding assistants and configures them automatically:

```bash
# Auto-detect all installed coding agents and configure them
python -m archon.cli init
```

To see which agents are currently detected on your machine:
```bash
python -m archon.cli detect
```

---

## 3. Targeted Manual Export

Export skills to a specific coding assistant:

```bash
# Export to Cursor
python -m archon.cli export --target cursor

# Export to Claude Code
python -m archon.cli export --target claude_code

# Export to Windsurf
python -m archon.cli export --target windsurf

# Export to GitHub Copilot
python -m archon.cli export --target copilot

# Export to Cline / Roo Code
python -m archon.cli export --target cline

# Export to Aider
python -m archon.cli export --target aider

# Export to all agents at once
python -m archon.cli export --target all
```

---

## 4. `skills.sh` Registry

Archon is fully compatible with the open `skills.sh` package ecosystem:

```bash
# Add to your project via npx skills
npx skills add archon-ai/archon-skills

# Install globally
npx skills add archon-ai/archon-skills --global
```
