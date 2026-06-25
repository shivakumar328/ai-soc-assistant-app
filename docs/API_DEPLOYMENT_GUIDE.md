# 🛡️ SOC Assistant REST API & Deployment Guide

---

## API DOCUMENTATION

### Base URL
```
Development: http://localhost:5000/api
Production: https://soc-assistant.company.com/api
```

### Authentication
All requests require Authorization header:
```
Authorization: Bearer TOKEN
```

---

## ENDPOINTS

### 1. Alerts Management

#### Get All Alerts
```http
GET /api/alerts
```

**Query Parameters:**
- `severity` (optional): critical, high, medium, low
- `limit` (default: 100): Number of results
- `offset` (default: 0): Pagination offset
- `source` (optional): SIEM source filter
- `status` (optional): open, investigating, closed

**Response:**
```json
{
  "alerts": [
    {
      "id": 1,
      "type": "SQL Injection Attempt",
      "source": "IDS-01",
      "severity": "critical",
      "timestamp": "2024-06-24T10:15:30Z",
      "description": "SQL injection pattern detected",
      "source_ip": "192.168.1.100",
      "target": "web-server-01",
      "status": "open"
    }
  ],
  "total": 1000,
  "page": 1
}
```

**Example:**
```bash
curl -H "Authorization: Bearer TOKEN" \
  "http://localhost:5000/api/alerts?severity=critical&limit=50"
```

---

#### Get Alert Details
```http
GET /api/alerts/{alert_id}
```

**Response:**
```json
{
  "id": 1,
  "type": "SQL Injection Attempt",
  "severity": "critical",
  "timestamp": "2024-06-24T10:15:30Z",
  "description": "SQL injection pattern detected in HTTP request",
  "source_ip": "192.168.1.100",
  "target": "web-server-01",
  "payload": "' OR '1'='1",
  "detection_method": "IDS Pattern Matching",
  "rule_id": "1000015",
  "source": "IDS-01",
  "status": "open",
  "assigned_to": null,
  "tags": ["sql-injection", "web-app", "critical"],
  "related_alerts": [2, 3, 5]
}
```

---

#### Update Alert Status
```http
PATCH /api/alerts/{alert_id}
```

**Request Body:**
```json
{
  "status": "investigating",
  "assigned_to": "soc-analyst-01",
  "tags": ["false-positive"],
  "notes": "Investigating potential false positive"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Alert updated successfully",
  "alert_id": 1
}
```

---

### 2. Alert Analysis

#### Analyze Alert with AI
```http
POST /api/analyze
```

**Request Body:**
```json
{
  "alert": {
    "type": "SQL Injection Attempt",
    "source_ip": "192.168.1.100",
    "target": "web-server-01",
    "payload": "' OR '1'='1"
  },
  "context": "security_operations"
}
```

**Response:**
```json
{
  "alert_id": 1,
  "threat_summary": "SQL injection attack detected targeting web application database. Attacker attempted to bypass authentication using classic payload.",
  "risk_level": "CRITICAL",
  "risk_score": 9.5,
  "recommendation": "Immediately isolate affected web server and review WAF logs",
  "evidence": [
    "Suspicious SQL characters in HTTP request",
    "Pattern matches known SQL injection attack",
    "Multiple attempts from same IP in short time"
  ],
  "investigation_steps": [
    "1. Check WAF logs for similar patterns",
    "2. Identify all requests from source IP",
    "3. Review application logs for unauthorized access",
    "4. Check for database modifications",
    "5. Verify if attack was successful"
  ],
  "mitre": {
    "tactics": ["Initial Access", "Execution"],
    "techniques": ["T1190: Exploit Public-Facing Application", "T1059: Command and Scripting Interpreter"]
  }
}
```

---

#### Get MITRE ATT&CK Mapping
```http
POST /api/mitre-mapping
```

**Request Body:**
```json
{
  "alert": {
    "type": "Lateral Movement",
    "description": "WMI event binding detected"
  }
}
```

**Response:**
```json
{
  "tactics": ["Persistence", "Execution"],
  "techniques": [
    {
      "id": "T1547.020",
      "name": "Boot or Logon Autostart Execution: WMI Event Subscription",
      "description": "Adversaries may establish persistence by executing malicious content triggered by WMI events"
    }
  ],
  "mitigations": [
    "M1047: Audit",
    "M1040: Behavior Prevention on Endpoint"
  ],
  "detection": "Monitor WMI event subscriptions and ActiveScriptEventConsumer objects"
}
```

---

### 3. Incident Response

#### Generate Incident Response Plan
```http
POST /api/incident-response
```

**Request Body:**
```json
{
  "alert": {
    "type": "Ransomware Detected",
    "source": "workstation-42",
    "severity": "critical"
  },
  "analysis": {
    "risk_level": "CRITICAL",
    "threat_summary": "Ransomware activity detected"
  }
}
```

**Response:**
```json
{
  "immediate_actions": [
    "1. ISOLATE: Disconnect affected system from network immediately",
    "2. PRESERVE: Collect forensic evidence before reboot",
    "3. ALERT: Notify incident response team and management",
    "4. DOCUMENT: Record timeline and findings"
  ],
  "containment_steps": [
    "Block process from spreading to other systems",
    "Disable network interfaces",
    "Isolate backup systems",
    "Monitor for lateral movement"
  ],
  "eradication_steps": [
    "Remove malware/ransomware samples",
    "Reset all compromised credentials",
    "Patch vulnerable systems",
    "Review and harden access controls"
  ],
  "recovery_steps": [
    "Restore from clean backups (after verification)",
    "Rebuild systems if necessary",
    "Gradually reconnect to network",
    "Monitor for re-infection"
  ],
  "lessons_learned": [
    "Improve endpoint detection and response",
    "Enhance backup and disaster recovery",
    "Conduct security awareness training",
    "Review access control policies"
  ],
  "communication_template": "At [TIME], ransomware was detected on workstation-42. The system has been isolated and IR team notified. Updates will be provided every 2 hours.",
  "escalation_criteria": "Contact executive leadership if: 1) Multiple systems affected, 2) Critical data encrypted, 3) Ransom note present"
}
```

---

### 4. Threat Intelligence

#### Get IOC Information
```http
GET /api/threat-intel/ioc/{ioc_value}
```

**Query Parameters:**
- `type`: ip, domain, hash, email
- `include_sources`: true/false

**Response:**
```json
{
  "ioc": "185.220.101.45",
  "type": "ip",
  "threat_level": "high",
  "reputation": "malicious",
  "first_seen": "2024-01-15T10:00:00Z",
  "last_seen": "2024-06-24T08:00:00Z",
  "sources": [
    {
      "source": "abuse.ch",
      "confidence": 95,
      "category": "botnet"
    },
    {
      "source": "virustotal",
      "confidence": 88,
      "category": "c2-server"
    }
  ],
  "associated_malware": ["Emotet", "Trickbot"],
  "campaigns": ["APT-29", "Cozy Bear"],
  "recommendations": "Block IP at firewall/WAF immediately"
}
```

---

#### Search Threat Feeds
```http
GET /api/threat-intel/search
```

**Query Parameters:**
- `query`: Search term
- `feed`: abuse.ch, virustotal, otx, misp
- `limit`: Results limit

**Response:**
```json
{
  "results": [
    {
      "indicator": "malware.com",
      "type": "domain",
      "feed": "abuse.ch",
      "threat_type": "malware-c2",
      "confidence": 95,
      "last_updated": "2024-06-24T10:00:00Z"
    }
  ],
  "total": 42
}
```

---

### 5. Logs & Audit

#### Search Logs
```http
GET /api/logs/search
```

**Query Parameters:**
- `query`: Search query
- `source`: Log source filter
- `start_time`: ISO 8601 timestamp
- `end_time`: ISO 8601 timestamp
- `limit`: 10-1000

**Response:**
```json
{
  "logs": [
    {
      "timestamp": "2024-06-24T10:15:30Z",
      "source": "web-server-01",
      "level": "ERROR",
      "message": "SQL injection attempt detected",
      "details": {
        "user": "unknown",
        "ip": "192.168.1.100",
        "method": "GET",
        "path": "/api/users?id=' OR '1'='1"
      }
    }
  ],
  "total": 156,
  "page": 1
}
```

---

### 6. Health & Status

#### System Health
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-06-24T10:15:30Z",
  "version": "1.0.0",
  "components": {
    "api": "healthy",
    "database": "healthy",
    "siem_connection": "healthy",
    "claude_api": "healthy"
  },
  "metrics": {
    "active_alerts": 42,
    "alerts_today": 156,
    "average_analysis_time": "3.2s",
    "uptime": "99.8%"
  }
}
```

---

## DEPLOYMENT GUIDES

### AWS Deployment

#### Using EC2 + RDS + ALB

```yaml
# Terraform configuration
provider "aws" {
  region = "us-east-1"
}

# Security Group
resource "aws_security_group" "soc_assistant" {
  name = "soc-assistant-sg"
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance
resource "aws_instance" "soc_assistant" {
  ami                    = "ami-0c55b159cbfafe1f0"
  instance_type          = "t3.xlarge"
  security_groups        = [aws_security_group.soc_assistant.name]
  key_name               = "your-key"
  
  user_data = file("user_data.sh")
  
  tags = {
    Name = "SOC-Assistant"
  }
}

# RDS Database
resource "aws_db_instance" "soc_db" {
  identifier     = "soc-assistant-db"
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.t3.medium"
  allocated_storage = 100
  
  db_name  = "soc_db"
  username = "admin"
  password = random_password.db_password.result
  
  skip_final_snapshot = false
}

# Application Load Balancer
resource "aws_lb" "soc_alb" {
  name               = "soc-assistant-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.soc_assistant.id]
  
  enable_deletion_protection = true
}
```

Deploy:
```bash
terraform init
terraform plan
terraform apply
```

---

### Google Cloud Deployment

```yaml
# GCP App Engine deployment
runtime: python39

env: standard

env_variables:
  ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY}
  DATABASE_URL: ${DATABASE_URL}

entrypoint: gunicorn soc_assistant_backend:app

handlers:
- url: /.*
  script: auto
  secure: always
  redirect_http_response_code: 301
```

Deploy:
```bash
gcloud app deploy
```

---

### Azure Deployment

```yaml
# Azure Container Instances
{
  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",
  "contentVersion": "1.0.0.0",
  "resources": [
    {
      "type": "Microsoft.ContainerInstance/containerGroups",
      "name": "soc-assistant",
      "location": "[resourceGroup().location]",
      "properties": {
        "containers": [
          {
            "name": "soc-backend",
            "properties": {
              "image": "soc-assistant:latest",
              "resources": {
                "requests": {
                  "cpu": 2,
                  "memoryInGB": 4
                }
              },
              "ports": [
                {
                  "port": 5000
                }
              ],
              "environmentVariables": [
                {
                  "name": "ANTHROPIC_API_KEY",
                  "secureValue": "[parameters('apiKey')]"
                }
              ]
            }
          }
        ],
        "osType": "Linux",
        "ipAddress": {
          "type": "Public",
          "ports": [
            {
              "protocol": "TCP",
              "port": 5000
            }
          ],
          "dnsNameLabel": "soc-assistant"
        }
      }
    }
  ]
}
```

---

### On-Premise Deployment

#### Hardware Requirements
```
CPU: 8-core processor (Intel Xeon or equivalent)
RAM: 32GB minimum (64GB recommended)
Storage: 1TB SSD for logs
Network: 10Gbps connection (minimum 1Gbps)
GPU: NVIDIA GPU for ML acceleration (optional)
```

#### Installation Script
```bash
#!/bin/bash
set -e

# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install dependencies
sudo apt-get install -y python3.9 python3-pip git postgresql postgresql-contrib

# Create application directory
sudo mkdir -p /opt/soc-assistant
sudo chown $USER:$USER /opt/soc-assistant
cd /opt/soc-assistant

# Clone repository
git clone https://github.com/your-org/soc-assistant.git .

# Setup Python environment
python3 -m venv venv
source venv/bin/activate

# Install Python packages
pip install -r requirements.txt

# Setup database
sudo -u postgres createdb soc_db
sudo -u postgres psql -d soc_db -f database/schema.sql

# Configure application
cp .env.example .env
nano .env  # Edit configuration

# Setup systemd service
sudo cp systemd/soc-assistant.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable soc-assistant
sudo systemctl start soc-assistant

# Setup Nginx reverse proxy
sudo apt-get install -y nginx
sudo cp nginx/soc-assistant.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/soc-assistant.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Setup SSL certificate
sudo apt-get install -y certbot python3-certbot-nginx
sudo certbot certonly --nginx -d soc-assistant.company.com

echo "Installation complete!"
```

---

### High Availability Setup

```yaml
# Load Balancing Configuration
upstream soc_backend {
    least_conn;
    server backend-1:5000;
    server backend-2:5000;
    server backend-3:5000;
}

server {
    listen 443 ssl http2;
    server_name soc-assistant.company.com;
    
    ssl_certificate /etc/letsencrypt/live/soc-assistant.company.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/soc-assistant.company.com/privkey.pem;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;
    
    location /api {
        proxy_pass http://soc_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
        
        # Rate limiting
        limit_req zone=api burst=20 nodelay;
    }
}

# Rate limiting
limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
```

---

### Monitoring & Logging

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
alerts_processed = Counter(
    'alerts_processed_total',
    'Total alerts processed',
    ['severity', 'source']
)

analysis_duration = Histogram(
    'analysis_seconds',
    'Time to analyze alert',
    buckets=(1, 2, 5, 10)
)

active_incidents = Gauge(
    'active_incidents',
    'Number of active incidents'
)

# Export metrics
@app.route('/metrics')
def metrics():
    return generate_latest()
```

---

### Backup & Disaster Recovery

```bash
#!/bin/bash
# Daily backup script

BACKUP_DIR="/backups/soc-assistant"
RETENTION_DAYS=30

# Database backup
pg_dump soc_db | gzip > $BACKUP_DIR/db_$(date +%Y%m%d).sql.gz

# Configuration backup
tar czf $BACKUP_DIR/config_$(date +%Y%m%d).tar.gz /opt/soc-assistant/.env

# Remove old backups
find $BACKUP_DIR -name "*.gz" -mtime +$RETENTION_DAYS -delete

# Verify backup integrity
gzip -t $BACKUP_DIR/db_$(date +%Y%m%d).sql.gz

# Upload to S3
aws s3 cp $BACKUP_DIR/ s3://backup-bucket/soc-assistant/ --recursive
```

---

**Version**: 1.0
**Last Updated**: June 2024
