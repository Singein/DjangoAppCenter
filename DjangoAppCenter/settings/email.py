"""邮件配置
"""
from DjangoAppCenter.settings.options import OPTIONS


email = OPTIONS.get('email')


EMAIL_SUBJECT_PREFIX = email.get('subject_prefix')
SERVER_EMAIL = email.get('server_email')
EMAIL_HOST = email.get('email_host')   # SMTP服务器
EMAIL_HOST_USER = email.get('email_host_user')  # 邮箱名
EMAIL_HOST_PASSWORD = email.get('email_host_password')  # 邮箱密码
EMAIL_PORT = email.get('email_port')    # 发送邮件的端口
EMAIL_USE_TLS = email.get('email_use_tls')    # 是否使用 TLS
EMAIL_FROM = email.get('email_from')   # 默认的发件人
ADMINS = email.get('admins')  # 邮件接收人，可以有多个
