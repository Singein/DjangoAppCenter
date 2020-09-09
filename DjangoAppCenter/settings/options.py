"""默认配置
"""

from DjangoAppCenter.settings.osprofile import OSProfile
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEFAULT_OPTIONS = {
    'admin_site_title': 'DjangoAppCenter',
    'admin_site_header': 'DjangoAppCenter',
    'allowed_host': '0.0.0.0',
    'port': 6666,
    'static_root': 'statics',  # 静态资源地址
    'redirect': 'admin/',  # 重定向
    'apps': [],
    'middlewares': [],
    "routers": [],
    'database_routers': [],
    'databases': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'db.sqlite3'
        }
    },
    'rest_framework': {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
        'PAGE_SIZE': 100,
        'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
    },
    'logs_dir': 'logs',
    'email': {
        'subject_prefix': 'DjangoAppCenter',
        'server_email': 'xxx@xxx.com',
        'email_host': 'smtp.163.com',
        'email_host_user': 'xxx@xxx.com',
        'email_host_password': 'xxxxxx',
        'email_port': 25,
        'email_use_tls': True,
        'email_from': 'xxx@xxx.com',
        'admins': [('xxx', 'xxx@xxx.com')]
    }
}


osprofile = OSProfile(appname="DjangoAppCenter",
                      profile="profile.json", options=DEFAULT_OPTIONS)

PROFILE_NAME = osprofile.profile
OPTIONS = osprofile.read_profile()
