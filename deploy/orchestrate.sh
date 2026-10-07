#!/usr/bin/env bash
set -euo pipefail

# KEDDEH.COM Deployment Orchestrator
# Complete deployment workflow from source to production runtime.

echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Starting deployment orchestration..."

ROOT="${ROOT:-.}"
ENV="${ENV:-production}"
DEPLOY_TARGET="${DEPLOY_TARGET:-/opt/keddeh/keddeh.com}"
DEPLOY_USER="${DEPLOY_USER:-keddeh}"

echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Environment: $ENV"
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Target: $DEPLOY_TARGET"
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] User: $DEPLOY_USER"

# Phase 1: Validate
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Phase 1: Validating runtime..."
cd "$ROOT"
python3 build.py validate || exit 1

# Phase 2: Generate manifest
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Phase 2: Generating deployment manifest..."
python3 build.py manifest > build/MANIFEST.json

# Phase 3: Initialize deployment environment
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Phase 3: Initializing deployment environment..."
if [ "$EUID" -eq 0 ]; then
  bash deploy/init.sh "$ROOT" || exit 1
else
  echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Note: Skipping system-level setup (requires root)"
  echo "[KEDDEH-DEPLOY-ORCHESTRATOR] To complete deployment, run: sudo bash deploy/init.sh"
fi

# Phase 4: TLS certificate setup
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Phase 4: Setting up TLS certificates..."
mkdir -p .certs
if [ ! -f ".certs/keddeh.crt" ]; then
  bash deploy/tls_manager.sh generate
else
  echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Certificate already exists"
fi

# Phase 5: DNS configuration
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Phase 5: Configuring DNS zones..."
bash deploy/dns_manager.sh init

# Phase 6: Health checks
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Phase 6: Running health checks..."
if bash deploy/health_check.sh; then
  echo "[KEDDEH-DEPLOY-ORCHESTRATOR] ✓ Health checks passed"
else
  echo "[KEDDEH-DEPLOY-ORCHESTRATOR] ⚠ Some health checks failed (expected if services not running)"
fi

echo ""
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Deployment orchestration complete!"
echo ""
echo "[KEDDEH-DEPLOY-ORCHESTRATOR] Next steps:"
echo "  1. Review configuration: cat build/MANIFEST.json"
echo "  2. Start service: systemctl start keddeh-runtime.service"
echo "  3. Enable on boot: systemctl enable keddeh-runtime.service"
echo "  4. Monitor: systemctl status keddeh-runtime.service"
echo "  5. View logs: journalctl -u keddeh-runtime.service -f"
echo ""
