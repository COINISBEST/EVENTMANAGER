import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime

# Create logs directory if it doesn't exist
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

# Configure logging
class SecurityFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, 'request'):
            record.request_data = json.dumps({
                'ip': getattr(record.request, 'client', {}).get('host', 'unknown'),
                'method': getattr(record.request, 'method', 'unknown'),
                'url': str(getattr(record.request, 'url', 'unknown')),
                'timestamp': datetime.utcnow().isoformat()
            })
        return super().format(record)

# Create logger
logger = logging.getLogger('event_management')
logger.setLevel(logging.INFO)

# Create handlers
file_handler = RotatingFileHandler(
    'logs/security.log',
    maxBytes=10485760,  # 10MB
    backupCount=5
)
console_handler = logging.StreamHandler()

# Create formatters
file_formatter = SecurityFormatter(
    '%(asctime)s - %(levelname)s - %(message)s - %(request_data)s'
)
console_formatter = logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'
)

# Set formatters
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler) 