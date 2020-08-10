import os
import sys
import fire


def debug():
    """Django's command-line utility for administrative tasks."""
    os.environ.setdefault('APP_CENTER_ENVIRON', 'DEBUG')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppCenter.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    args = [''] + sys.argv[2:]
    execute_from_command_line(args)


def prod():
    # TODO 后期修改为 uwsgi部署
    """Django's command-line utility for administrative tasks."""

    os.environ.setdefault('APP_CENTER_ENVIRON', 'PROD')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AppCenter.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    args = [''] + sys.argv[2:]
    execute_from_command_line(args)


def entry():
    fire.Fire({
        'debug': debug,
        'prod': prod
    })
