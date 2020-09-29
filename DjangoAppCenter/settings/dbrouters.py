"""数据库读写分离定义
"""

from django.conf import settings

apps = getattr(settings, 'INSTALLED_APPS', [])


class Router:
    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label == 'settings':
            return 'settings'
        if app_label in apps:
            return app_label
        return 'default'

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label == 'settings':
            return 'settings'
        if app_label in apps:
            return app_label
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return True

    def allow_migrate(self, db, applabel, **hints):
        return True
