import json
import logging
import os
import sqlite3
from abc import abstractmethod, ABC

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = {
    "SERVED_HOSTS": "0.0.0.0",
    "PORT": 8000,
    "ROUTERS": [],
    "LANGUAGE_CODE": "zh-hans",
    "TIME_ZONE": "Asia/Shanghai",
    "USE_I18N": True,
    "USE_L10N": True,
    "USE_TZ": True,
    "LOGS_DIR": "logs"
}


class DjangoAppCenterSettingStorageError(Exception):
    pass


class DjangoAppCenterSettingStorage(ABC):

    @abstractmethod
    def load(self) -> dict:
        pass


class DjangoAppCenterSettingSqliteStorage(DjangoAppCenterSettingStorage):
    BASE_DB_PATH = os.path.join(os.path.abspath(os.getcwd()), "DjangoAppCenter.sqlite3")

    def __init__(self):
        if not os.path.exists(self.BASE_DB_PATH):
            logger.error("Database not found, please run 'python manage.py migrate' first.")

    def load(self) -> dict:
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect(self.BASE_DB_PATH)
            cursor = conn.cursor()

            # Execute a query to find the latest config_snapshot
            cursor.execute("SELECT config FROM config_snapshot WHERE latest = 1 ORDER BY publish_time DESC LIMIT 1")
            result = cursor.fetchone()

            # Close the connection
            conn.close()

            if result:
                # Parse the JSON string into a Python dictionary
                DEFAULT_SETTINGS.update(json.loads(result[0]))
                return DEFAULT_SETTINGS
            else:
                return DEFAULT_SETTINGS
        except sqlite3.Error as e:
            logger.error(f"Database error: {e}")
            return DEFAULT_SETTINGS
        except Exception as e:
            logger.error(f"General error: {e}")
            return DEFAULT_SETTINGS


django_app_center_settings_storage = DjangoAppCenterSettingSqliteStorage()

django_app_center_settings = django_app_center_settings_storage.load()
