import json
import os
import sqlite3

BASE_SETTING_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SETTINGS_DB_PATH = os.path.join(BASE_SETTING_DIR, "databases", "settings.sqlite3")
DEFAULT_DB_PATH = os.path.join(BASE_SETTING_DIR, "databases", "db.sqlite3")
CWD_SETTINGS_DB_PATH = os.path.join(os.path.abspath(os.getcwd()), "settings.sqlite3")
CWD_DB_PATH = os.path.join(os.path.abspath(os.getcwd()), "db.sqlite3")
PROFILE = "settings.json"


class SettingsLoadingError:
    pass


def get_settings_dbcfg() -> dict:
    return {
        "settings": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": DEFAULT_SETTINGS_DB_PATH if not os.path.exists(CWD_SETTINGS_DB_PATH) else CWD_SETTINGS_DB_PATH
        }
    }


def load_settings_from_db() -> dict:
    if os.path.exists(CWD_SETTINGS_DB_PATH):
        connection = sqlite3.connect(CWD_SETTINGS_DB_PATH)
    else:
        connection = sqlite3.connect(DEFAULT_SETTINGS_DB_PATH)

    cursor = connection.cursor()
    cursor.execute("select * from settings_settings")
    result = cursor.fetchall()
    settings = {}
    settings.update({"LOGGING": LOGGING})
    for r in result:
        key = r[1]
        raw_json = r[2]
        try:
            settings[key] = json.loads(raw_json)
        except:
            settings[key] = raw_json

    return settings


def load_settings_from_file() -> dict:
    settings_path = os.path.join(os.getcwd(), "settings.json")
    settings = dict()
    settings.update({"LOGGING": LOGGING})
    settings.update(json.loads(open(settings_path, encoding="utf-8").read()))
    return settings
