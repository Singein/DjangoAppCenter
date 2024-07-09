import json
import os
from datetime import datetime

from settings import BASE_DIR


class PackageEventHandler:
    TOUCH_RELOAD_FILE = os.path.join(BASE_DIR, 'package-event.log')

    @staticmethod
    def write_event(func):
        def wrapper():
            event = func()
            with open(PackageEventHandler.TOUCH_RELOAD_FILE, 'w') as f:
                f.write(f'{json.dumps(event, ensure_ascii=False)}\n')

        return wrapper

    @staticmethod
    @write_event
    def on_package_installed(package_name: str,
                             package_version: str,
                             old_config_snapshot_version: str,
                             new_config_snapshot_version: str):
        return {
            'event': 'package_installed',
            'package_name': package_name,
            'package_version': package_version,
            'old_config_snapshot_version': old_config_snapshot_version,
            'new_config_snapshot_version': new_config_snapshot_version,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    @write_event
    def on_package_uninstalled(package_name: str,
                               package_version: str,
                               old_config_snapshot_version: str,
                               new_config_snapshot_version: str):
        return {
            'event': 'package_uninstalled',
            'package_name': package_name,
            'package_version': package_version,
            'old_config_snapshot_version': old_config_snapshot_version,
            'new_config_snapshot_version': new_config_snapshot_version,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    @staticmethod
    def on_package_updated(package_name: str,
                           package_old_version: str,
                           package_new_version: str,
                           old_config_snapshot_version: str,
                           new_config_snapshot_version: str):
        return {
            'event': 'package_updated',
            'package_name': package_name,
            'package_old_version': package_old_version,
            'package_new_version': package_new_version,
            'old_config_snapshot_version': old_config_snapshot_version,
            'new_config_snapshot_version': new_config_snapshot_version,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
