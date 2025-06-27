import json
import re
from django.core.exceptions import ImproperlyConfigured


from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    "version": 1,
    'disable_existing_loggers': False,
    "filters": {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {name}  {message}",
            "style": "{",
        },
        "verbose": {
            "format": "{levelname} {asctime} {name} {module}.py (line {lineno:d}) {funcName} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / 'logs' / "django.log",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "filters": ["require_debug_false"],
            "formatter": "verbose",
            "include_html": True,
        },
    },
    "loggers": {
        "": {
            "level": "INFO",
            "handlers": ["console", "file", "mail_admins"],
        },
        "django": {
            "level": "INFO",
            "handlers": ["console", "file", "mail_admins"],
            "propagate": False,
        },
        "django.templates": {
            "level": "DEBUG",
            "handlers": ["file"],
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["console", "file", "mail_admins"],
            "level": "ERROR",
            "propagate": False,
        },
    }
}


def parse_admins_json(json_string):
    if not json_string.strip():
        return []

    try:
        admin_list = json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ImproperlyConfigured(f"Invalid JSON in ADMINS_JSON: {e}")

    if not isinstance(admin_list, list):
        raise ImproperlyConfigured("ADMINS_JSON must be a JSON array")

    admins = []
    email_regex = re.compile(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

    for i, admin in enumerate(admin_list):
        if not isinstance(admin, dict):
            raise ImproperlyConfigured(f"Admin {i+1} must be a JSON object")

        if 'name' not in admin or 'email' not in admin:
            raise ImproperlyConfigured(
                f"Admin {i+1} missing 'name' or 'email' field")

        name = str(admin['name']).strip()
        email = str(admin['email']).strip().lower()

        if not email_regex.match(email):
            raise ImproperlyConfigured(
                f"Admin {i+1} has invalid email format: {email}")

        admins.append((name, email))

    # Check for duplicate emails
    emails = [admin[1] for admin in admins]
    if len(emails) != len(set(emails)):
        raise ImproperlyConfigured(
            "Duplicate email addresses found in ADMINS_JSON")

    return admins
