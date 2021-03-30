import re


def get_python_version():
    import subprocess
    p = subprocess.Popen(['python', '--version'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()

    # 为了兼容 python 2.x 中 python --version 输出到 stderr 的bug
    # https://bugs.python.org/issue18338
    stdout = stderr if not stdout else stdout

    version = re.findall(r'([0-9]+)\.([0-9]+)\.([0-9\+]+)', str(stdout))[0]

    import platform
    if (not platform.system() == 'Windows') and version[0] == '2':
        return 'python3'

    return 'python'
