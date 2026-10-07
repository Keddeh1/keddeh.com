#!/usr/bin/env bash
set -euo pipefail

# KEDDEH.COM DNS Zone Configuration Manager
# Manages DNS record definitions for KEDDEH.COM and subdomains.

echo "[KEDDEH-DNS-ZONE] DNS configuration manager"

ZONE_FILE="${ZONE_FILE:-./deploy/dns/keddeh.com.zone}"
CONFIG_FILE="${CONFIG_FILE:-./deploy/dns/keddeh.com.conf}"

case "${1:-list}" in
  init)
    echo "[KEDDEH-DNS-ZONE] Initializing DNS zone files..."
    mkdir -p "$(dirname "$ZONE_FILE")"
    mkdir -p "$(dirname "$CONFIG_FILE")"

    cat > "$ZONE_FILE" <<'EOF'
; KEDDEH.COM DNS Zone File
; Custom local DNS runtime configuration

; SOA Record (Start of Authority)
@ 3600 IN SOA ns1.keddeh.com. admin.keddeh.com. (
  2026100701 ; serial
  3600       ; refresh
  1800       ; retry
  604800     ; expire
  86400      ; minimum TTL
)

; NS Records (Name Servers)
@ 3600 IN NS ns1.keddeh.com.
@ 3600 IN NS ns2.keddeh.com.

; A Records (IPv4)
@ 3600 IN A 127.0.0.1
www 3600 IN A 127.0.0.1
dns 3600 IN A 127.0.0.1
ns1 3600 IN A 127.0.0.1
ns2 3600 IN A 127.0.0.1

; AAAA Records (IPv6) - optional
@ 3600 IN AAAA ::1
www 3600 IN AAAA ::1

; MX Records (Mail Exchange)
@ 3600 IN MX 10 mail.keddeh.com.

; CNAME Records
mail 3600 IN CNAME @

; TXT Records
@ 3600 IN TXT "v=spf1 -all"
EOF
    echo "[KEDDEH-DNS-ZONE] Zone file created: $ZONE_FILE"

    cat > "$CONFIG_FILE" <<'EOF'
{
  "zone": "keddeh.com",
  "ttl": 3600,
  "soa": {
    "primary_ns": "ns1.keddeh.com",
    "admin_email": "admin@keddeh.com",
    "serial": 2026100701,
    "refresh": 3600,
    "retry": 1800,
    "expire": 604800,
    "minimum_ttl": 86400
  },
  "nameservers": [
    "ns1.keddeh.com",
    "ns2.keddeh.com"
  ],
  "records": {
    "a": {
      "@": "127.0.0.1",
      "www": "127.0.0.1",
      "dns": "127.0.0.1",
      "ns1": "127.0.0.1",
      "ns2": "127.0.0.1"
    },
    "aaaa": {
      "@": "::1",
      "www": "::1"
    },
    "mx": {
      "@": {"priority": 10, "server": "mail.keddeh.com"}
    },
    "cname": {
      "mail": "@"
    }
  },
  "runtime": "custom_local",
  "custom_runtime": true,
  "github_dependencies": false
}
EOF
    echo "[KEDDEH-DNS-ZONE] Configuration created: $CONFIG_FILE"
    ;;

  list)
    echo "[KEDDEH-DNS-ZONE] DNS records for keddeh.com:"
    if [ -f "$CONFIG_FILE" ]; then
      python3 -m json.tool "$CONFIG_FILE" | grep -A 50 '"records"' || true
    else
      echo "[KEDDEH-DNS-ZONE] Configuration file not found. Run 'init' first."
    fi
    ;;

  validate)
    echo "[KEDDEH-DNS-ZONE] Validating DNS configuration..."
    if [ ! -f "$CONFIG_FILE" ]; then
      echo "[KEDDEH-DNS-ZONE] ERROR: Configuration not found"
      exit 1
    fi
    python3 -m json.tool "$CONFIG_FILE" >/dev/null && echo "[KEDDEH-DNS-ZONE] ✓ Configuration valid" || echo "[KEDDEH-DNS-ZONE] ✗ Invalid JSON"
    ;;

  *)
    echo "Usage: $0 {init|list|validate}"
    exit 1
    ;;
esac
