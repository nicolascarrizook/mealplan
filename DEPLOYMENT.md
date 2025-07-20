# Deployment Guide - Meal Planner Application

## Prerequisites

- A DigitalOcean Droplet (Ubuntu 20.04 or 22.04 recommended)
- SSH access to your droplet
- A domain name (optional, but recommended for production)
- OpenAI API key

## Quick Deployment Steps

### 1. Connect to your Droplet

```bash
ssh root@your-droplet-ip
```

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/apptresdiasycarga.git
cd apptresdiasycarga
```

### 3. Run the Installation Script

```bash
chmod +x install-on-droplet.sh
./install-on-droplet.sh
```

This script will:
- Install Docker and Docker Compose
- Install and configure Nginx
- Setup firewall rules
- Create necessary directories

### 4. Configure Environment Variables

Edit the `.env` file with your configuration:

```bash
nano .env
```

Required configurations:
- `OPENAI_API_KEY`: Your OpenAI API key
- `VITE_API_URL`: Replace with `http://your-droplet-ip:8000`
- Update CORS_ORIGINS with your droplet IP

### 5. Deploy the Application

```bash
./deploy.sh
```

### 6. Update Nginx Configuration

Edit the nginx configuration with your domain or IP:

```bash
sudo nano /etc/nginx/sites-available/meal-planner
```

Replace `your-domain.com` with your actual domain or droplet IP.

Restart Nginx:
```bash
sudo systemctl restart nginx
```

## SSL/HTTPS Setup (Recommended)

For production deployments, setup SSL using Certbot:

```bash
sudo snap install --classic certbot
sudo certbot --nginx
```

Follow the prompts to secure your domain with Let's Encrypt SSL certificate.

## Managing the Application

### View logs
```bash
docker-compose logs -f
```

### Stop the application
```bash
docker-compose down
```

### Restart the application
```bash
docker-compose restart
```

### Update the application
```bash
git pull origin main
./deploy.sh
```

## Troubleshooting

### Check if services are running
```bash
docker-compose ps
```

### Check nginx status
```bash
sudo systemctl status nginx
```

### View nginx error logs
```bash
sudo tail -f /var/log/nginx/error.log
```

### Reset and redeploy
```bash
docker-compose down -v
docker system prune -a
./deploy.sh
```

## Backup

To backup your data:

```bash
# Backup PDFs
tar -czf pdfs-backup-$(date +%Y%m%d).tar.gz pdfs/

# Backup environment config
cp .env .env.backup-$(date +%Y%m%d)
```

## Security Recommendations

1. **Change default SSH port** in `/etc/ssh/sshd_config`
2. **Disable root login** and use a sudo user
3. **Enable automatic security updates**:
   ```bash
   sudo apt-get install unattended-upgrades
   sudo dpkg-reconfigure --priority=low unattended-upgrades
   ```
4. **Regular backups** of your data and configuration
5. **Monitor logs** for suspicious activity

## Support

For issues or questions:
1. Check the logs first: `docker-compose logs`
2. Verify your .env configuration
3. Ensure all ports are properly configured in your firewall