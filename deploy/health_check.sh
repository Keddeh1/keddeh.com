#!/usr/bin/env bash
set -euo pipefail

# KEDDEH.COM Health and Monitoring Checks
# Validates runtime service health across HTTPS, HTTP, DNS, and custom execution fabric.

echo "[KEDDEH-MONITOR] Running comprehensive health checks..."

HTTPS_PORT=${HTTPS_PORT:-443}
HTTP_PORT=${HTTP_PORT:-80}
DNS_PORT=${DNS_PORT:-5300}
HEALTH_LOG="${HEALTH_LOG:-/tmp/keddeh-health.log}"

echo "[KEDDEH-MONITOR] Timestamp: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$HEALTH_LOG"

# Check HTTPS Service
echo "[KEDDEH-MONITOR] Checking HTTPS (port $HTTPS_PORT)..."
if timeout 5 curl -k -s -o /dev/null -w "%{http_code}" https://127.0.0.1:$HTTPS_PORT/ 2>/dev/null | grep -q "200\|301"; then
  echo "[KEDDEH-MONITOR] ✓ HTTPS service: healthy" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ HTTPS service: UNHEALTHY" | tee -a "$HEALTH_LOG"
fi

# Check HTTP Redirect
echo "[KEDDEH-MONITOR] Checking HTTP redirect (port $HTTP_PORT)..."
if timeout 5 curl -s -o /dev/null -w "%{http_code}" -L http://127.0.0.1:$HTTP_PORT/ 2>/dev/null | grep -q "301\|200"; then
  echo "[KEDDEH-MONITOR] ✓ HTTP redirect: healthy" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ HTTP redirect: UNHEALTHY" | tee -a "$HEALTH_LOG"
fi

# Check DNS Service
echo "[KEDDEH-MONITOR] Checking DNS (port $DNS_PORT)..."
if timeout 5 dig @127.0.0.1 -p $DNS_PORT keddeh.com A +short 2>/dev/null | grep -q "127.0.0.1"; then
  echo "[KEDDEH-MONITOR] ✓ DNS service: healthy" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ DNS service: UNHEALTHY" | tee -a "$HEALTH_LOG"
fi

# Check KEX state geometry
echo "[KEDDEH-MONITOR] Checking KEX state geometry..."
if python3 -c "from runtime.local_runtime.kex_geometry import KEXStateGeometry; KEXStateGeometry('.')" >/dev/null 2>&1; then
  echo "[KEDDEH-MONITOR] ✓ KEX runtime: initialized" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ KEX runtime: UNINITIALIZED" | tee -a "$HEALTH_LOG"
fi

# Check BRAINK execution fabric
echo "[KEDDEH-MONITOR] Checking BRAINK execution fabric..."
if python3 -c "from runtime.local_runtime.braink_fabric import BRAINKExecutionFabric; BRAINKExecutionFabric('.')" >/dev/null 2>&1; then
  echo "[KEDDEH-MONITOR] ✓ BRAINK fabric: operational" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ BRAINK fabric: INOPERATIONAL" | tee -a "$HEALTH_LOG"
fi

# Check IL-LLM semantic substrate
echo "[KEDDEH-MONITOR] Checking IL-LLM semantic substrate..."
if python3 -c "from runtime.local_runtime.il_llm_semantic import ILLMSemanticSubstrate; ILLMSemanticSubstrate('.')" >/dev/null 2>&1; then
  echo "[KEDDEH-MONITOR] ✓ IL-LLM substrate: initialized" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ IL-LLM substrate: UNINITIALIZED" | tee -a "$HEALTH_LOG"
fi

# Check Mesh topology
echo "[KEDDEH-MONITOR] Checking Mesh topology coordinator..."
if python3 -c "from runtime.local_runtime.mesh_topology import MeshTopologyCoordinator; MeshTopologyCoordinator('.')" >/dev/null 2>&1; then
  echo "[KEDDEH-MONITOR] ✓ Mesh topology: initialized" | tee -a "$HEALTH_LOG"
else
  echo "[KEDDEH-MONITOR] ✗ Mesh topology: UNINITIALIZED" | tee -a "$HEALTH_LOG"
fi

echo "[KEDDEH-MONITOR] Health check complete. Log: $HEALTH_LOG"
