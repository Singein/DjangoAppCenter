package = {
    'name': 'DjangoAppCenter',
    'version': '0.9.17',
    'author': 'singein',
    'email': 'singein@outlook.com',
    'scripts': {
        'default': 'echo 请输入明确的命令名称',
        'migrate': 'python -m DjangoAppCenter makemigrations && python -m DjangoAppCenter migrate',
        'upload': 'twine upload --repository-url=http://0.9.17.46:5555 --trusted-host=0.9.17.46'
    }
}
