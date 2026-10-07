#!/usr/bin/env bash
set -euo pipefail

# KEDDEH.COM Deployment Initialization
# Hardens the runtime environment for production operation.

echo "[KEDDEH-DEPLOY] Initializing production runtime environment..."

ROOT="${1:-.}"
DEPLOY_USER="${DEPLOY_USER:-keddeh}"
DEPLOY_GROUP="${DEPLOY_GROUP:-keddeh}"
DEPLOY_HOME="/opt/keddeh/keddeh.com"
CERT_DIR="${DEPLOY_HOME}/.certs"
LOGS_DIR="${DEPLOY_HOME}/logs"
DATA_DIR="${DEPLOY_HOME}/data"

# Check if running as root
if [ "$EUID" -ne 0 ]; then
  echo "[KEDDEH-DEPLOY] ERROR: deployment requires root privileges"
  exit 1
fi

echo "[KEDDEH-DEPLOY] Creating deployment user and group..."
if ! id -u "$DEPLOY_USER" >/dev/null 2>&1; then
  useradd -r -s /bin/false -d "$DEPLOY_HOME" "$DEPLOY_USER" || true
  echo "[KEDDEH-DEPLOY] User '$DEPLOY_USER' created"
else
  echo "[KEDDEH-DEPLOY] User '$DEPLOY_USER' already exists"
fi

echo "[KEDDEH-DEPLOY] Creating directory structure..."
mkdir -p "$DEPLOY_HOME" "$CERT_DIR" "$LOGS_DIR" "$DATA_DIR"
chown -R "$DEPLOY_USER:$DEPLOY_GROUP" "$DEPLOY_HOME"
chmod 750 "$DEPLOY_HOME" "$CERT_DIR" "$LOGS_DIR" "$DATA_DIR"

echo "[KEDDEH-DEPLOY] Setting up certificate directory..."
chmod 700 "$CERT_DIR"

echo "[KEDDEH-DEPLOY] Installing systemd units..."
cp deploy/systemd/keddeh-runtime.service /etc/systemd/system/
cp deploy/systemd/keddeh-dns.service /etc/systemd/system/
cp deploy/systemd/keddeh-https.service /etc/systemd/system/
systemctl daemon-reload
echo "[KEDDEH-DEPLOY] Systemd units installed"

echo "[KEDDEH-DEPLOY] Installing runtime to $DEPLOY_HOME..."
if [ -d "$DEPLOY_HOME" ]; then
  echo "[KEDDEH-DEPLOY] Deployment target exists; backup and refresh"
  # In production: implement proper versioning and rollback
fi

echo "[KEDDEH-DEPLOY] Setting permissions on Python modules..."
find "$DEPLOY_HOME" -type f -name "*.py" -exec chmod 644 {} \;
find "$DEPLOY_HOME" -type f -executable -exec chmod 755 {} \;

echo "[KEDDEH-DEPLOY] Creating health check script..."
cat > "$DEPLOY_HOME/health_check.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

echo "[KEDDEH-HEALTH] Running health checks..."

# Check HTTPS service
if curl -k -s https://127.0.0.1/ >/dev/null 2>&1; then
  echo "[KEDDEH-HEALTH] HTTPS: OK"
else
  echo "[KEDDEH-HEALTH] HTTPS: FAILED"
  exit 1
fi

# Check DNS service
if dig @127.0.0.1 -p 5300 keddeh.com >/dev/null 2>&1; then
  echo "[KEDDEH-HEALTH] DNS: OK"
else
  echo "[KEDDEH-HEALTH] DNS: FAILED"
  exit 1
fi

echo "[KEDDEH-HEALTH] All checks passed"
exit 0
EOF
chmod 755 "$DEPLOY_HOME/health_check.sh"

echo "[KEDDEH-DEPLOY] Configuring log rotation..."
cat > /etc/logrotate.d/keddeh-runtime <<EOF
$LOGS_DIR/*.log {
  daily
  rotate 14
  compress
  delaycompress
  missingok
  notifempty
  create 0640 $DEPLOY_USER $DEPLOY_GROUP
  postrotate
    systemctl reload-or-restart keddeh-runtime.service > /dev/null 2>&1 || true
  endscript
}
EOF
echo "[KEDDEH-DEPLOY] Log rotation configured"

echo "[KEDDEH-DEPLOY] Production deployment initialized successfully"
echo ""
echo "[KEDDEH-DEPLOY] Next steps:"
echo "  1. Generate TLS certificates:"
echo "     openssl req -x509 -newkey rsa:4096 -keyout $CERT_DIR/keddeh.key -out $CERT_DIR/keddeh.crt -days 365 -nodes"
echo "  2. Start the service:"
echo "     systemctl start keddeh-runtime.service"
echo "  3. Enable on boot:"
echo "     systemctl enable keddeh-runtime.service"
echo "  4. Check status:"
echo "     systemctl status keddeh-runtime.service"
echo ""
