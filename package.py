package = {
    'name': 'DjangoAppCenter',
    'version': '0.4.0',
    'author': 'singein',
    'email': 'singein@outlook.com',
    'scripts': {
        'default': 'echo 请输入明确的命令名称',
        'migrate': 'python -m DjangoAppCenter makemigrations && python -m DjangoAppCenter migrate',
        'upload': 'twine upload --repository-url=http://0.4.0.46:5555 --trusted-host=0.4.0.46'
    }
}
