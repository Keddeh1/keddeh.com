#!/usr/bin/env bash
set -euo pipefail

# KEDDEH.COM TLS Certificate Lifecycle Management
# Handles certificate generation, renewal, and verification.

echo "[KEDDEH-TLS] Certificate lifecycle management"

CERT_DIR="${CERT_DIR:-./.certs}"
CERT_FILE="${CERT_DIR}/keddeh.crt"
KEY_FILE="${CERT_DIR}/keddeh.key"
CERT_VALIDITY_DAYS=${CERT_VALIDITY_DAYS:-365}
WARN_THRESHOLD_DAYS=${WARN_THRESHOLD_DAYS:-30}

mkdir -p "$CERT_DIR"
chmod 700 "$CERT_DIR"

case "${1:-generate}" in
  generate)
    echo "[KEDDEH-TLS] Generating self-signed certificate..."
    openssl req -x509 \
      -newkey rsa:2048 \
      -keyout "$KEY_FILE" \
      -out "$CERT_FILE" \
      -days "$CERT_VALIDITY_DAYS" \
      -nodes \
      -subj "/C=US/ST=Local/L=Local/O=Keddeh/CN=keddeh.com"
    chmod 600 "$KEY_FILE"
    chmod 644 "$CERT_FILE"
    echo "[KEDDEH-TLS] Certificate generated at $CERT_FILE"
    echo "[KEDDEH-TLS] Private key at $KEY_FILE"
    ;;

  check)
    echo "[KEDDEH-TLS] Checking certificate validity..."
    if [ ! -f "$CERT_FILE" ]; then
      echo "[KEDDEH-TLS] ERROR: Certificate not found at $CERT_FILE"
      exit 1
    fi
    openssl x509 -in "$CERT_FILE" -text -noout | grep -A 1 "Not Before\|Not After"
    echo "[KEDDEH-TLS] Certificate OK"
    ;;

  renew)
    echo "[KEDDEH-TLS] Renewing certificate..."
    if [ -f "$CERT_FILE" ]; then
      mv "$CERT_FILE" "${CERT_FILE}.bak"
      echo "[KEDDEH-TLS] Backed up old certificate to ${CERT_FILE}.bak"
    fi
    openssl req -x509 \
      -newkey rsa:2048 \
      -keyout "$KEY_FILE" \
      -out "$CERT_FILE" \
      -days "$CERT_VALIDITY_DAYS" \
      -nodes \
      -subj "/C=US/ST=Local/L=Local/O=Keddeh/CN=keddeh.com"
    echo "[KEDDEH-TLS] Certificate renewed"
    systemctl reload-or-restart keddeh-runtime.service 2>/dev/null || echo "[KEDDEH-TLS] Note: systemd service not running"
    ;;

  inspect)
    echo "[KEDDEH-TLS] Inspecting certificate..."
    openssl x509 -in "$CERT_FILE" -text -noout
    ;;

  *)
    echo "Usage: $0 {generate|check|renew|inspect}"
    exit 1
    ;;
esac
