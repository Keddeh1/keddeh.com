# KEDDEH.COM Deployment Configuration

Production hardening and deployment configuration for KEDDEH.COM sovereign runtime.

## Directory Structure

```
deploy/
├── init.sh                 # Production deployment initialization
├── health_check.sh         # Comprehensive health monitoring
├── tls_manager.sh          # TLS certificate lifecycle management
├── dns_manager.sh          # DNS zone configuration
├── orchestrate.sh          # Complete deployment orchestration
├── systemd/
│   ├── keddeh-runtime.service    # Unified runtime service
│   ├── keddeh-dns.service        # DNS service
│   └── keddeh-https.service      # HTTPS service
└── dns/
    ├── keddeh.com.zone          # DNS zone file
    └── keddeh.com.conf          # DNS configuration
```

## Deployment Workflow

### Quick Start (Single Command)

```bash
sudo bash deploy/orchestrate.sh
```

This runs the complete deployment pipeline:
1. Validates runtime components
2. Generates deployment manifest
3. Initializes system environment (requires root)
4. Sets up TLS certificates
5. Configures DNS zones
6. Runs health checks

### Manual Deployment Steps

#### 1. Initialize Production Environment

```bash
sudo bash deploy/init.sh
```

Creates:
- `keddeh` system user and group
- `/opt/keddeh/keddeh.com` deployment directory
- Required subdirectories with proper permissions
- systemd service units
- Log rotation configuration

#### 2. Manage TLS Certificates

```bash
# Generate self-signed certificate (development)
bash deploy/tls_manager.sh generate

# Check certificate validity
bash deploy/tls_manager.sh check

# Renew certificate
bash deploy/tls_manager.sh renew

# Inspect certificate details
bash deploy/tls_manager.sh inspect
```

#### 3. Configure DNS Zones

```bash
# Initialize DNS zone files
bash deploy/dns_manager.sh init

# List current records
bash deploy/dns_manager.sh list

# Validate DNS configuration
bash deploy/dns_manager.sh validate
```

#### 4. Run Health Checks

```bash
bash deploy/health_check.sh
```

Verifies:
- HTTPS service (port 443)
- HTTP redirect (port 80)
- UDP DNS (port 5300)
- KEX state geometry
- BRAINK execution fabric
- IL-LLM semantic substrate
- Mesh topology coordinator

## Service Management

### Using systemd

```bash
# Start the unified runtime
sudo systemctl start keddeh-runtime.service

# Enable on boot
sudo systemctl enable keddeh-runtime.service

# Check status
sudo systemctl status keddeh-runtime.service

# View logs
sudo journalctl -u keddeh-runtime.service -f

# Restart service
sudo systemctl restart keddeh-runtime.service
```

### Individual Services

```bash
# Start DNS service
sudo systemctl start keddeh-dns.service

# Start HTTPS service
sudo systemctl start keddeh-https.service

# Check all services
sudo systemctl status keddeh-*.service
```

## Production Hardening

### Security Features

- **Process isolation**: Dedicated `keddeh` system user
- **Capability binding**: Only `CAP_NET_BIND_SERVICE` for ports < 1024
- **Private `/tmp`**: Each process gets isolated temporary filesystem
- **No new privileges**: Prevents privilege escalation
- **Automatic restart**: Configured recovery on failure
- **Resource limits**: Start limit of 5 restarts per 60 seconds
- **Logging**: All output to systemd journal with tags

### TLS/HTTPS

- **Self-signed certificates**: Auto-generated on first run
- **TLS 1.3**: Modern encryption standard
- **HSTS headers**: Strict-Transport-Security enforced
- **Certificate lifecycle**: Renewal scripts included

### DNS

- **UDP port 5300**: Standard DNS resolution
- **Zone configuration**: JSON-based DNS record management
- **Local resolution**: All domains resolve to 127.0.0.1
- **Record types**: A, AAAA, CNAME, MX support

### Monitoring

- **Health checks**: Comprehensive service validation
- **Log rotation**: 14-day retention with compression
- **Automatic logging**: systemd journal integration
- **Service watchdog**: Automatic restart on failure

## Environment Variables

```bash
DEPLOY_USER=keddeh              # System user for services
DEPLOY_GROUP=keddeh            # System group for services
DEPLOY_TARGET=/opt/keddeh/keddeh.com  # Deployment root
CERT_VALIDITY_DAYS=365         # Certificate validity period
WARN_THRESHOLD_DAYS=30         # Certificate expiration warning
HTTPS_PORT=443                 # HTTPS service port
HTTP_PORT=80                   # HTTP redirect port
DNS_PORT=5300                  # DNS UDP port
```

## Production Checklist

- [ ] Run deployment orchestration: `sudo bash deploy/orchestrate.sh`
- [ ] Verify systemd services: `systemctl status keddeh-*.service`
- [ ] Test HTTPS: `curl -k https://127.0.0.1/`
- [ ] Test DNS: `dig @127.0.0.1 -p 5300 keddeh.com`
- [ ] Check logs: `journalctl -u keddeh-runtime.service`
- [ ] Run health checks: `bash deploy/health_check.sh`
- [ ] Set up certificate renewal cron: `crontab -e`
- [ ] Configure firewall rules (if applicable)
- [ ] Set up monitoring/alerting

## Troubleshooting

### Service won't start

```bash
sudo journalctl -u keddeh-runtime.service -n 50
```

### Port already in use

```bash
sudo lsof -i :443
sudo lsof -i :80
sudo lsof -i :5300
```

### DNS not resolving

```bash
dig @127.0.0.1 -p 5300 keddeh.com
nslookup keddeh.com 127.0.0.1:5300
```

### Certificate errors

```bash
bash deploy/tls_manager.sh check
bash deploy/tls_manager.sh inspect
```

## License

KEDDEH Systems Custom Runtime License - Sovereign Platform
