import json
import os
from shutil import copyfile

BASE_SETTING_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_SETTINGS_PATH = os.path.join(BASE_SETTING_DIR, "templates", "settings.default.json")
DEFAULT_DB_PATH = os.path.join(BASE_SETTING_DIR, "templates", "db.default.sqlite3")

CWD_DB_PATH = os.path.join(os.path.abspath(os.getcwd()), "db.default.sqlite3")
CWD_SETTINGS_PATH = os.path.join(os.path.abspath(os.getcwd()), "settings.json")


def get_default_database() -> dict:
    return {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": DEFAULT_DB_PATH if not os.path.exists(CWD_DB_PATH) else CWD_DB_PATH
        }
    }


def load_settings_from_file() -> dict:
    settings_path = CWD_SETTINGS_PATH if os.path.exists(CWD_SETTINGS_PATH) else DEFAULT_SETTINGS_PATH
    return json.loads(open(settings_path, encoding="utf-8").read())


def init_profile():
    cwd = os.getcwd()
    dockerfile = os.path.join(os.path.abspath(cwd), "Dockerfile")

    if not os.path.exists(CWD_SETTINGS_PATH):
        copyfile(DEFAULT_SETTINGS_PATH, CWD_SETTINGS_PATH)

    if not os.path.exists(CWD_DB_PATH):
        copyfile(DEFAULT_DB_PATH, CWD_DB_PATH)

    if not os.path.exists(dockerfile):
        copyfile(os.path.join(BASE_SETTING_DIR, "templates", "Dockerfile"), dockerfile)
