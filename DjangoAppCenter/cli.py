import os
import sys

import fire

from DjangoAppCenter.settings.loader import init_profile
from DjangoAppCenter.settings.loader import load_settings_from_db

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))


def dev():
    """run django in debug mode"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAppCenter.settings')
    os.environ.setdefault('DAC_ENVIRON', 'DEV')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    args = [''] + sys.argv[2:]
    execute_from_command_line(args)


def prod():
    """run django in production mode"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoAppCenter.settings')
    os.environ.setdefault('DAC_ENVIRON', 'PROD')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Couldn't import Django.") from exc
    args = [''] + sys.argv[2:]
    execute_from_command_line(args)


def deploy_nginx():
    """
    run django with uwsgi
    """
    os.environ.setdefault('DAC_ENVIRON', 'PROD')
    custom_settings = load_settings_from_db()
    static_root = custom_settings.get('static_root', 'statics')
    wsgi_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "settings", 'wsgi.py')
    allowed_host = custom_settings.get('DAC_SERVED_HOSTS', '0.0.0.0')
    port = custom_settings.get('PORT', 8888)
    os.system("python -m DjangoAppCenter prod collectstatic --noinput")
    os.system("uwsgi --py-autoreload=1 --socket=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" % (
        allowed_host, str(port), wsgi_path, static_root))


def deploy():
    """
    run django with uwsgi
    """
    os.environ.setdefault('DAC_ENVIRON', 'PROD')
    custom_settings = load_settings_from_db()
    static_root = custom_settings.get('static_root', 'statics')
    wsgi_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "settings", 'wsgi.py')
    served_hosts = custom_settings.get('DAC_SERVED_HOSTS', '0.0.0.0')
    port = custom_settings.get('PORT', 8888)
    os.system("python -m DjangoAppCenter prod collectstatic --noinput")
    os.system("uwsgi --py-autoreload=1 --http=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" % (
        served_hosts, str(port), wsgi_path, static_root))


def entry():
    fire.Fire({
        'dev': dev,
        'prod': prod,
        'deploy': deploy,
        'nginx': deploy_nginx,
        'init': init_profile
    })
