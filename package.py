package = {
    'name': 'DjangoAppCenter',
    'version': '0.3.11',
    'author': 'singein',
    'email': 'singein@outlook.com',
    'scripts': {
        'default': 'echo 请输入明确的命令名称',
        'migrate': 'python -m DjangoAppCenter makemigrations && python -m DjangoAppCenter migrate',
        'upload': 'twine upload --repository-url=http://8.210.201.46:5555 --trusted-host=8.210.201.46'
    }
}
