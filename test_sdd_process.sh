#!/bin/bash
# Helper to run the E2E simulation and provide the Hub UI link

set -e

# Resolve the active Jetski daemon port
PORT_FILE="$HOME/.gemini/jetski/daemon_port"
PORT=""

if [ -f "$PORT_FILE" ]; then
  # Parse port from daemon lockfile
  PORT=$(cat "$PORT_FILE" | tr -d ' \n\r' | grep -o 'port:[0-9]*' | cut -d: -f2 || true)
fi

if [ -z "$PORT" ]; then
  # Fallback to checking active ports using ss
  PORT=$(ss -tlpn 2>/dev/null | grep -o ':[0-9]\+ ' | tr -d ' ' | head -n1 | cut -d: -f2 || true)
fi

if [ -z "$PORT" ]; then
  echo -e "\033[1;31m[Error]\033[0m Jetski Language Server daemon does not appear to be running."
  echo "Please start the standalone daemon first by running:"
  echo "  jetski web start"
  exit 1
fi

echo -e "\033[1;32m[Simulation Server Detected]\033[0m Running on port: $PORT"
echo "------------------------------------------------------------"
echo "👉 Open Jetski Hub in your browser to watch the simulation live:"
echo "   http://localhost:$PORT/"
echo "------------------------------------------------------------"
echo ""

# Parse arguments
PHASE=""
FIXTURE=""
CLEAN_MODE=false
CLEAN_TARGET=""

while [[ "$#" -gt 0 ]]; do
  case $1 in
    --phase) PHASE="$2"; shift ;;
    --fixture) FIXTURE="$2"; shift ;;
    --clean)
      CLEAN_MODE=true
      if [[ -n "$2" && ! "$2" =~ ^- ]]; then
        CLEAN_TARGET="$2"
        shift
      else
        CLEAN_TARGET="."
      fi
      ;;
    -h|--help)
      echo "Usage: ./test_sdd_process.sh [options]"
      echo "Options:"
      echo "  --phase <name>     Run isolated test phase (bootstrap, blueprint, reconciliation, security, implementation)"
      echo "  --fixture <file>   Run chained E2E with a custom fixture (e.g. generative_guestbook.json)"
      echo "  --clean [path]     Deregister the project from Jetski Hub and delete the directory on disk (defaults to current dir)"
      exit 0
      ;;
    *) echo "Unknown parameter: $1"; exit 1 ;;
  esac
  shift
  # Skip one shift if we processed an option with shifted argument
done

if [ "$CLEAN_MODE" = true ]; then
  python3 tests/cleanup_project.py "$CLEAN_TARGET"
  exit 0
fi

# Run the python simulator
if [ -n "$PHASE" ]; then
  echo "Running isolated simulation phase: $PHASE..."
  case $PHASE in
    bootstrap) python3 tests/sim_1_bootstrap.py ;;
    blueprint) python3 tests/sim_2_blueprint.py ;;
    reconciliation) python3 tests/sim_3_reconciliation.py ;;
    security) python3 tests/sim_4_permission_isolation.py ;;
    implementation) python3 tests/sim_5_implementation.py ;;
    *) echo "Unknown phase: $PHASE"; exit 1 ;;
  esac
else
  echo "Running chained end-to-end simulation..."
  if [ -n "$FIXTURE" ]; then
    python3 tests/sim_sdd_process.py --fixture "$FIXTURE"
  else
    python3 tests/sim_sdd_process.py
  fi
fi
