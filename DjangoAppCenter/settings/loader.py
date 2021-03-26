import json
import logging
import os
from shutil import copyfile

logger = logging.getLogger("admin")

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


def merge_profile(app: str, options: str):
    if not options:
        return
    try:
        options = json.loads(options)
        if not isinstance(options, dict):
            logger.error(f"App[{app}] 配置文件解析错误 {options}")
            return

        with open(CWD_SETTINGS_PATH, 'r', encoding="utf-8") as f:
            profile = json.loads(f.read())
            for key, value in options.items():
                if isinstance(value, (list, tuple)):
                    profile.update(**{key: list(set(profile.get(key, []) + value))})

                elif isinstance(value, dict):
                    if not profile.get(key, None):
                        profile[key] = {}
                    profile[key].update(**value)

                else:
                    profile.update(**{key: value})

        with open(CWD_SETTINGS_PATH, 'w', encoding="utf-8") as f:
            f.write(json.dumps(profile, ensure_ascii=False, indent=2))

        logger.info(f"App[{app}] settings success injected")

    except json.JSONDecodeError:
        logger.error(f"App[{app}] 配置文件解析错误 {options}")


def init_profile():
    cwd = os.getcwd()
    dockerfile = os.path.join(os.path.abspath(cwd), "Dockerfile")

    if not os.path.exists(CWD_SETTINGS_PATH):
        copyfile(DEFAULT_SETTINGS_PATH, CWD_SETTINGS_PATH)

    if not os.path.exists(CWD_DB_PATH):
        copyfile(DEFAULT_DB_PATH, CWD_DB_PATH)

    if not os.path.exists(dockerfile):
        copyfile(os.path.join(BASE_SETTING_DIR, "templates", "Dockerfile"), dockerfile)
