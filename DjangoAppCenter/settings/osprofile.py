__version__ = "0.2.1"

import json
import os
import platform


class OSProfileError(BaseException):
    pass


class OSProfile:

    def __init__(self, appname: str = None, profile: str = None, options: dict = None, path: str = '.'):


        if appname is not None and profile is not None:

            paths = [path, 'USER_HOME', '.']
            # cwd_profile_path = os.path.join(os.path.abspath(os.getcwd()), '%s.%s'%(appname, profile))
            for path in paths:
                if path == '.':
                    self.path = os.path.abspath(os.getcwd())
                    self.profile = '%s.%s' % (appname, profile)
                    break

                # Unix style profile path
                elif 'USER_HOME' == path:
                    if platform.system() != 'Windows':
                        self.path = os.path.join(
                            os.environ['HOME'], '.config', appname)
                        self.profile = profile

                    # Windows style profile path
                    else:
                        self.path = os.path.join(
                            os.environ['USERPROFILE'], 'AppData', 'Local', appname)

                        self.profile = profile
                    break

                else:
                    if not os.path.isdir(path):
                        continue
                    self.path = path
                    self.profile = profile
                    break

            self.options = options
            self._init_profile()

        else:
            raise OSProfileError('OSProfile init error.')

    def _init_profile(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        if not self.profile in os.listdir(self.path):
            with open(os.path.join(self.path, self.profile), 'w') as f:
                f.write(json.dumps(self.options, ensure_ascii=False, indent=4))

    def read_profile(self):
        with open(os.path.join(self.path, self.profile), 'r', encoding="utf-8") as f:
            return json.loads(f.read())

    def update_profile(self, kwargs):
        profile = self.read_profile()
        for key, value in zip(kwargs.keys(), kwargs.values()):
            profile[key] = value

        with open(os.path.join(self.path, self.profile), 'w', encoding="utf-8") as f:
            f.write(json.dumps(profile, ensure_ascii=False, indent=4))
