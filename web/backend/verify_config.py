from app.core.config import settings
import sys

print(f"SMTP_HOST='{settings.SMTP_HOST}'")
print(f"SMTP_USER='{settings.SMTP_USER}'")
print(f"SMTP_PASSWORD='{settings.SMTP_PASSWORD}'")
