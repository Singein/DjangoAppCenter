bind = "127.0.0.1:8000"
workers = 1

threads = 1  # 指定每个工作者的线程数
proc_name = 'DjangoAppCenter'  # 进程名称
worker_class = 'gevent'  # 工作模式协程
timeout = 30  # 超时
max_requests = 666  # 最大请求数
max_requests_jitter = 6
