#!/usr/bin/env bash
# Archon One-Command Zero-Friction Installer (macOS & Linux)
# Zero external dependencies. Uses system Python 3.

set -e

BOLD="\033[1m"
CYAN="\033[36m"
GREEN="\033[32m"
RED="\033[31m"
RESET="\033[0m"

echo -e "${CYAN}${BOLD}"
echo "==========================================================="
echo "              ARCHON SKILL SUITE INSTALLER                 "
echo "==========================================================="
echo -e "${RESET}"

# 1. Verify Python 3
PYTHON=""
if command -v python3 >/dev/null 2>&1; then
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON="python"
else
    echo -e "${RED}[ERROR] Python 3 is required but not installed.${RESET}" >&2
    exit 1
fi

PY_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "[✓] Found Python ${BOLD}${PY_VERSION}${RESET} ($PYTHON)"

# 2. Determine install paths
ARCHON_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DIR="$HOME/.local/bin"
mkdir -p "$BIN_DIR"

# 3. Create symlink or launcher
LAUNCHER="$BIN_DIR/archon"
cat <<EOF > "$LAUNCHER"
#!/usr/bin/env sh
export PYTHONPATH="$ARCHON_DIR:\$PYTHONPATH"
exec "$PYTHON" -m archon.cli "\$@"
EOF
chmod +x "$LAUNCHER"
echo -e "[✓] Installed executable wrapper to ${BOLD}$LAUNCHER${RESET}"

# Check PATH
case ":$PATH:" in
    *":$BIN_DIR:"*) ;;
    *) echo -e "${CYAN}[i] Note: Ensure $BIN_DIR is in your PATH environment variable.${RESET}" ;;
esac

# 4. Run Archon Initialization & Agent Discovery
echo -e "\n${BOLD}--- Auto-Detecting & Configuring AI Coding Agents ---${RESET}"
"$PYTHON" -m archon.cli init

echo -e "\n${GREEN}${BOLD}[✓] Archon installation completed successfully!${RESET}"
echo -e "Run ${BOLD}archon dashboard${RESET} or ${BOLD}archon council \"<proposal>\"${RESET} to begin."
