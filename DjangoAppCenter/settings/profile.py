import json
import logging
import os

logger = logging.getLogger("admin")


class SettingsLoaderError(Exception):
    pass


class SettingsLoader:

    def __init__(self, path: str):
        if not os.path.exists(path):
            raise SettingsLoaderError("Profile path not found")

        self.settings_path = path

    def load(self):
        try:
            return json.loads(open(self.settings_path, encoding="utf-8").read())
        except json.JSONDecodeError:
            raise SettingsLoaderError("Json decode failed.") from json.JSONDecodeError

    def merge(self, app: str, options: str):
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
                        try:
                            profile.update(**{key: list(set(profile.get(key, []) + value))})
                        except TypeError:
                            profile.update(**{key: profile.get(key, []) + value})

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
