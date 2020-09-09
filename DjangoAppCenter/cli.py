import os
import json
import sys
import fire
from DjangoAppCenter.settings import OPTIONS, PROFILE_NAME, DEFAULT_OPTIONS, DOCKER_FILE_TEMPLATE


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))


def debug():
    """run django in debug mode"""
    os.environ.setdefault('APP_CENTER_ENVIRON', 'DEBUG')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAppCenter.settings')
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
    """run django in production mode"""

    os.environ.setdefault('APP_CENTER_ENVIRON', 'PROD')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAppCenter.settings')
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


def deploy():
    """
    run django with uwsgi
    """

    os.environ.setdefault('APP_CENTER_ENVIRON', 'PROD')

    static_root = OPTIONS.get('static_root')
    wsgi_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "settings", 'wsgi.py')

    allowed_host = OPTIONS.get('allowed_host')
    port = OPTIONS.get('port')
    os.system(
        "python -m DjangoAppCenter prod collectstatic --noinput")
    os.system("uwsgi --http=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" %
              (allowed_host, str(port), wsgi_path, static_root))


def init_profile():
    cwd = os.getcwd()
    profile = os.path.join(os.path.abspath(cwd), PROFILE_NAME)
    dockerfile = os.path.join(os.path.abspath(cwd), "Dockerfile")

    if not os.path.exists(profile):
        with open(profile, "w", encoding="utf-8") as f:
            f.write(json.dumps(DEFAULT_OPTIONS))

    if not os.path.exists(dockerfile):
        with open(dockerfile, "w", encoding="utf-8") as f:
            f.write(json.dumps(DOCKER_FILE_TEMPLATE))


def entry():
    fire.Fire({
        'debug': debug,
        'prod': prod,
        'deploy': deploy,
        'init': init_profile
    })
