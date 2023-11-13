#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

"""from django.core.management import call_command
from django.core.management import setup_environ

try:
     from . import import_data
except ImportError:
    pass

# Autodiscover runscript management commands in all installed apps
call_command('runscript', 'setup')

# setup_environ() is required for using runscript in some cases.
setup_environ(None)
"""
def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
