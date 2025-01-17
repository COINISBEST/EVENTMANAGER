#!/bin/bash
set -e

# Load environment variables
source .env.production

# Set backup directory
BACKUP_DIR="backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory if it doesn't exist
mkdir -p $BACKUP_DIR

# Backup database
echo "Creating database backup..."
docker-compose -f docker-compose.prod.yml exec -T db \
    pg_dump -U $DB_USER $DB_NAME > "$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Backup uploaded files (if any)
echo "Creating files backup..."
tar -czf "$BACKUP_DIR/files_backup_$TIMESTAMP.tar.gz" uploads/

# Keep only last 7 backups
find $BACKUP_DIR -name "db_backup_*" -mtime +7 -delete
find $BACKUP_DIR -name "files_backup_*" -mtime +7 -delete

echo "Backup completed successfully!" 