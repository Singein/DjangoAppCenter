import os
import re
import sys

import fire

from DjangoAppCenter.settings.loader import init_profile, CWD_SETTINGS_PATH
from DjangoAppCenter.settings.loader import load_settings_from_file

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.getcwd()))


def get_python_version():
    import subprocess
    p = subprocess.Popen(['python', '--version'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()

    # 为了兼容 python 2.x 中 python --version 输出到 stderr 的bug
    # https://bugs.python.org/issue18338
    stdout = stderr if not stdout else stdout

    version = re.findall(r'([0-9]+)\.([0-9]+)\.([0-9\+]+)', str(stdout))[0]

    import platform
    if (not platform.system() == 'Windows') and version[0] == '2':
        return 'python3'

    return 'python'


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


def deploy(reload: bool = True, use_nginx: bool = False):
    """
    run django with uwsgi
    """
    os.environ.setdefault('DAC_ENVIRON', 'PROD')
    custom_settings = load_settings_from_file()
    static_root = custom_settings.get('STATIC_ROOT', 'statics')
    wsgi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'wsgi.py')
    served_hosts = custom_settings.get('DAC_SERVED_HOSTS', '0.0.0.0')
    port = custom_settings.get('PORT', 8000)
    os.system("%s -m DjangoAppCenter prod collectstatic --noinput" % get_python_version())
    if use_nginx:
        if reload:
            os.system(
                "uwsgi --py-autoreload=1 --touch-reload=%s --socket=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" % (
                    CWD_SETTINGS_PATH, served_hosts, str(port), wsgi_path, static_root))
        else:
            os.system(
                "uwsgi --touch-reload=%s --socket=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" % (
                    served_hosts, str(port), wsgi_path, static_root))
    else:
        if reload:
            os.system(
                "uwsgi --py-autoreload=1 --touch-reload=%s --http=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" % (
                    CWD_SETTINGS_PATH, served_hosts, str(port), wsgi_path, static_root))
        else:
            os.system(
                "uwsgi --touch-reload=%s --http=%s:%s --file=%s  --static-map=/static=%s --logto appcenter-wsgi.log" % (
                    served_hosts, str(port), wsgi_path, static_root))


def entry():
    fire.Fire({
        'dev': dev,
        'prod': prod,
        'deploy': deploy,
        'init': init_profile
    })
