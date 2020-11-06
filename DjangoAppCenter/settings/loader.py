import json
import os
import sqlite3
from shutil import copyfile

BASE_SETTING_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SETTINGS_DB_PATH = os.path.join(BASE_SETTING_DIR, "databases", "settings.sqlite3")
DEFAULT_SETTINGS_PATH = os.path.join(BASE_SETTING_DIR, "settings.default.json")
DEFAULT_DB_PATH = os.path.join(BASE_SETTING_DIR, "databases", "db.sqlite3")
CWD_SETTINGS_DB_PATH = os.path.join(os.path.abspath(os.getcwd()), "settings.sqlite3")
CWD_DB_PATH = os.path.join(os.path.abspath(os.getcwd()), "db.sqlite3")
PROFILE = "settings.json"
CWD_SETTINGS_PATH = os.path.join(BASE_SETTING_DIR, PROFILE)


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
    for r in result:
        key = r[1]
        raw_json = r[2]
        try:
            settings[key] = json.loads(raw_json)
        except json.JSONDecodeError:
            settings[key] = raw_json

    return settings


def load_settings_from_file() -> dict:
    settings_path = CWD_SETTINGS_PATH if os.path.exists(CWD_SETTINGS_PATH) else DEFAULT_SETTINGS_PATH
    return json.loads(open(settings_path, encoding="utf-8").read())
    

def load_settings() -> dict:
    # environment = os.environ.get("APP_CENTER_ENVIRON")
    # if environment == "DEV":
    #     return load_settings_from_file()
    #
    # elif environment == "PROD":
    #     return load_settings_from_db()
    #
    # else:
    #     return load_settings_from_file()

    return load_settings_from_file()


def init_profile():
    cwd = os.getcwd()
    profile = os.path.join(os.path.abspath(cwd), PROFILE)
    dockerfile = os.path.join(os.path.abspath(cwd), "Dockerfile")
    docker_template = load_settings_from_db().get("DOCKER_TEMPLATE")

    if not os.path.exists(profile):
        copyfile(os.path.join(BASE_SETTING_DIR, "settings.default.json"), profile)

    if not os.path.exists(CWD_SETTINGS_DB_PATH):
        copyfile(DEFAULT_SETTINGS_DB_PATH, CWD_SETTINGS_DB_PATH)

    if not os.path.exists(CWD_DB_PATH):
        copyfile(DEFAULT_DB_PATH, CWD_DB_PATH)

    if not os.path.exists(dockerfile):
        with open(dockerfile, "w", encoding="utf-8") as f:
            f.write(docker_template)
