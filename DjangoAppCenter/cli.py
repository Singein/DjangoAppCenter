import os
import sys
import fire
from DjangoAppCenter.settings import OPTIONS

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))


def debug():
    """Django's command-line utility for administrative tasks."""
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
    """Django's command-line utility for administrative tasks."""

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
    # CMD ["uwsgi", "--socket=127.0.0.1:6666", "--file=jzdw/wsgi.py", "--static-map=/static=jzdw/static", "--logto", "uwsgi.log"]

    os.environ.setdefault('APP_CENTER_ENVIRON', 'PROD')

    static_root = OPTIONS.get('static_root')
    wsgi_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "settings", 'wsgi.py')
    os.system(
        "python -m DjangoAppCenter prod collectstatic --noinput")
    os.system("uwsgi --http=0.0.0.0:6666 --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" %
              (wsgi_path, static_root))


def entry():
    fire.Fire({
        'debug': debug,
        'prod': prod,
        'deploy': deploy
    })
