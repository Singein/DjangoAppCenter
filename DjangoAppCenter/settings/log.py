import os

from DjangoAppCenter.settings.options import OPTIONS

logs_dir = OPTIONS.get('logs_dir')
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '%(asctime)s %(threadName)s:%(thread)d task_id:%(name)s %(filename)s:%(lineno)d %(levelname)s: %(message)s'
        },
        # 简单的日志格式
        'simple': {
            'format': '%(asctime)s %(levelname)s %(filename)s:%(lineno)d %(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
            'include_html': True,
            'formatter': 'standard'
        },
        'mail_admins_info': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
            # 'email_backend': 'django.core.mail.backends.smtp.EmailBackend',
            'include_html': True,
            'formatter': 'standard'
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            # 日志文件
            'filename': os.path.join(logs_dir, "appcenter.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'standard',
            'encoding': 'utf-8'
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            # 日志文件
            'filename': os.path.join(logs_dir, "appcenter-error.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(logs_dir, "appcenter-collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            # 上线之后可以把'console'移除
            'handlers': ['default', 'console', 'error', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        'collect': {
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        },
        'admin': {
            'handlers': ['mail_admins', 'mail_admins_info', 'error'],
            'level': 'INFO'
        }
    }
}
