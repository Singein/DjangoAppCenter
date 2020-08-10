"""数据库读写分离定义
"""


class Router:
    def db_for_read(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in ['sessions', 'auth', 'admin', 'contenttypes']:
            return 'default'
        return app_label

    def db_for_write(self, model, **hints):
        app_label = model._meta.app_label
        if app_label in ['sessions', 'auth', 'admin', 'contenttypes']:
            return 'default'
        return app_label
