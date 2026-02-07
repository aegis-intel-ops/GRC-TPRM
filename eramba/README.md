# Eramba Base Layer

This directory contains the Docker configuration for **Eramba Community Edition**, the open-source GRC platform that serves as the foundation of our GRC-TPRM solution.

## Quick Start

### 1. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit if needed (optional)
nano .env
```

### 2. Start Eramba

```bash
# Start the container
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f
```

### 3. Access Eramba

Open your browser and navigate to:
- **URL**: `http://localhost:80` (or custom port from `.env`)
- **Initial Setup**: Follow the on-screen wizard on first access

### 4. Default Credentials

After setup, you'll create an admin account. Keep these credentials secure.

## Container Management

### Stop Eramba
```bash
docker compose stop
```

### Restart Eramba
```bash
docker compose restart
```

### Remove Eramba (keeps data)
```bash
docker compose down
```

### Remove Everything (including data)
```bash
docker compose down -v
# WARNING: This deletes all vendor data, questionnaires, etc.
```

## Data Persistence

Data is stored in Docker volumes:
- `eramba_data`: Application files and uploads
- `eramba_db`: MySQL database

### Backup Data

```bash
# Backup database
docker compose exec eramba mysqldump -u root eramba > backup_$(date +%Y%m%d).sql

# Backup application data
docker run --rm -v eramba_eramba_data:/data -v $(pwd):/backup ubuntu tar czf /backup/eramba_data_$(date +%Y%m%d).tar.gz /data
```

### Restore Data

```bash
# Restore database
cat backup_20260206.sql | docker compose exec -T eramba mysql -u root eramba

# Restore application data
docker run --rm -v eramba_eramba_data:/data -v $(pwd):/backup ubuntu tar xzf /backup/eramba_data_20260206.tar.gz -C /
```

## Troubleshooting

### Container won't start

```bash
# Check logs for errors
docker compose logs

# Common issues:
# - Port 80 already in use: Change ERAMBA_PORT in .env
# - Insufficient memory: Ensure Docker has at least 2GB RAM
```

### Cannot access web interface

```bash
# Check if container is running
docker compose ps

# Check if port is accessible
curl -I http://localhost:80

# If using custom port, ensure .env is loaded
docker compose down && docker compose up -d
```

### Database errors

```bash
# Restart the container
docker compose restart

# If persistent, check volume integrity
docker volume inspect eramba_eramba_db
```

## Updating Eramba

```bash
# Pull latest image
docker compose pull

# Recreate container with new image
docker compose up -d

# Note: Always backup before updating!
```

## Configuration

Eramba configuration is managed through:
1. **Web Interface**: Most settings via admin panel
2. **Environment Variables**: Basic settings via `.env`
3. **Docker Compose**: Container configuration

## Integration with Other Layers

The Intelligence Layer will integrate with Eramba via:
- **REST API**: Eramba provides API endpoints (requires configuration)
- **Database**: Direct read-only access to vendor data (advanced)
- **Webhooks**: Event notifications (if configured)

## Resources

- [Eramba Documentation](https://www.eramba.org/documentation)
- [Eramba Community Forums](https://www.eramba.org/forums)
- [Docker Hub - Eramba](https://hub.docker.com/r/eramba/community)

## Notes

- Eramba uses PHP and CakePHP framework
- Default database is MySQL (embedded in container)
- First startup may take 2-3 minutes
- Initial setup wizard only appears once
