# AutoBlogger Deployment Guide

## Overview

This guide covers deploying AutoBlogger to production environments, including:
- Server requirements
- Installation process
- Configuration
- Security best practices
- Monitoring and maintenance

---

## Server Requirements

### Minimum Requirements
- **OS:** Linux (Ubuntu 20.04+), Windows Server 2019+, or macOS
- **Python:** 3.10 or higher
- **RAM:** 2GB minimum, 4GB recommended
- **Disk:** 10GB+ for application and logs
- **Network:** HTTPS-enabled web server (Nginx/Apache recommended)

### Recommended Requirements
- **RAM:** 8GB+
- **CPU:** 2+ cores
- **Disk:** SSD with 50GB+ space
- **Backup:** Automated backup system

---

## Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/your-org/autoblogger.git
cd autoblogger
```

### Step 2: Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Run Deployment Script

```bash
python deploy.py
```

This script will:
- Check Python version
- Install dependencies
- Create necessary directories
- Set up configuration files
- Run initial tests

### Step 4: Configure Environment

Edit `.env` file with your credentials:

```bash
# AI Provider
GEMINI_API_KEY=your_actual_key_here

# Image Services
UNSPLASH_ACCESS_KEY=your_actual_key_here

# Application Security
AUTOBLOGGER_SECRET_KEY=generate_a_random_key

# Flask Configuration
FLASK_ENV=production
FLASK_DEBUG=false

# Security
ALLOWED_HOSTS=yourdomain.com
CORS_ORIGINS=https://yourdomain.com
RATE_LIMIT_ENABLED=true
```

### Step 5: Configure Application

Edit `config/settings.json`:

```json
{
  "ai_provider": "gemini",
  "publisher": "file",
  "environment": "production",
  "log_level": "INFO",
  "max_posts_per_day": 10,
  "request_timeout": 60,
  "blogs": [
    {
      "id": "your_blog",
      "niche": "your niche",
      "target_audience": "your audience",
      "tone": "professional",
      "posts_per_week": 3,
      "keywords": ["keyword1", "keyword2"],
      "word_count": 1500,
      "publish_to": "file"
    }
  ]
}
```

---

## Web Server Setup

### Using Nginx (Recommended)

1. Install Nginx:
```bash
sudo apt update
sudo apt install nginx
```

2. Create Nginx configuration:

```nginx
# /etc/nginx/sites-available/autoblogger

server {
    listen 80;
    server_name yourdomain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # SSL certificates (use Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    location / {
        proxy_pass http://127.0.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    location /static {
        alias /path/to/autoblogger/static;
        expires 30d;
    }
}
```

3. Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/autoblogger /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Using Apache

```apache
# /etc/apache2/sites-available/autoblogger.conf

<VirtualHost *:80>
    ServerName yourdomain.com
    Redirect permanent / https://yourdomain.com/
</VirtualHost>

<VirtualHost *:443>
    ServerName yourdomain.com
    
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/yourdomain.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/yourdomain.com/privkey.pem
    
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:5001/
    ProxyPassReverse / http://127.0.0.1:5001/
    
    <Directory />
        Require all granted
    </Directory>
</VirtualHost>
```

---

## Process Management

### Using Systemd (Linux)

Create a systemd service file:

```ini
# /etc/systemd/system/autoblogger.service

[Unit]
Description=AutoBlogger Web Service
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/path/to/autoblogger
Environment="PATH=/path/to/autoblogger/venv/bin"
ExecStart=/path/to/autoblogger/venv/bin/python web_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable autoblogger
sudo systemctl start autoblogger
sudo systemctl status autoblogger
```

### Using Supervisor

```ini
# /etc/supervisor/conf.d/autoblogger.conf

[program:autoblogger]
command=/path/to/autoblogger/venv/bin/python web_app.py
directory=/path/to/autoblogger
user=www-data
autostart=true
autorestart=true
stderr_logfile=/var/log/autoblogger/err.log
stdout_logfile=/var/log/autoblogger/out.log
```

---

## Security Checklist

- [ ] All API keys stored in .env (never in code)
- [ ] HTTPS enabled with valid SSL certificate
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation in place
- [ ] File upload restrictions configured
- [ ] Error messages don't expose sensitive info
- [ ] Logs don't contain API keys or passwords
- [ ] Regular security updates applied

---

## Monitoring

### Log Files

Monitor these log files:
- `logs/autoblogger.log` - Application logs
- `/var/log/nginx/access.log` - Web server access
- `/var/log/nginx/error.log` - Web server errors

### Health Checks

Set up automated health checks:
```bash
# Check if service is responding
curl -f https://yourdomain.com/health || alert

# Monitor disk space
df -h | grep '/dev/sda1' | awk '{print $5}' | sed 's/%//' > /tmp/disk_usage
```

### Metrics to Monitor

- Request rate and latency
- Error rate
- API call failures
- Disk space usage
- Memory usage
- CPU usage

---

## Backup Strategy

### Automated Backups

```bash
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/autoblogger"

# Backup configuration
cp -r /path/to/autoblogger/config "$BACKUP_DIR/config_$DATE"

# Backup output files
cp -r /path/to/autoblogger/output "$BACKUP_DIR/output_$DATE"

# Backup logs
cp -r /path/to/autoblogger/logs "$BACKUP_DIR/logs_$DATE"

# Remove backups older than 30 days
find "$BACKUP_DIR" -name "config_*" -mtime +30 -delete
find "$BACKUP_DIR" -name "output_*" -mtime +30 -delete
```

Add to crontab:
```bash
0 2 * * * /path/to/backup.sh
```

---

## Scaling

### Horizontal Scaling

To handle more traffic:

1. Use a load balancer (Nginx, HAProxy)
2. Run multiple AutoBlogger instances
3. Share configuration via network storage
4. Use Redis for rate limiting across instances

### Vertical Scaling

- Increase server resources (CPU, RAM)
- Optimize database queries
- Enable caching
- Use CDN for static assets

---

## Troubleshooting

### Application Won't Start

```bash
# Check logs
tail -f logs/autoblogger.log

# Check service status
sudo systemctl status autoblogger

# Test configuration
python -c "from src.utils.config_loader import load_config; load_config()"
```

### High Memory Usage

```bash
# Check process memory
ps aux | grep python

# Monitor in real-time
htop

# Restart service
sudo systemctl restart autoblogger
```

### API Rate Limiting

If you're hitting API limits:
- Increase refill rate in rate limiter
- Add more API keys and rotate
- Cache API responses
- Reduce generation frequency

---

## Maintenance

### Regular Tasks

**Daily:**
- Check logs for errors
- Monitor disk space
- Verify backups completed

**Weekly:**
- Review security logs
- Update dependencies (if needed)
- Check for API changes

**Monthly:**
- Security audit
- Performance review
- Backup testing

### Updates

```bash
# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Update dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart autoblogger
```

---

## Support

For issues and support:
- GitHub Issues: https://github.com/your-org/autoblogger/issues
- Documentation: See `docs/` directory
- Email: support@yourdomain.com

---

**Last Updated:** October 2025
**Version:** 1.0.0

