DOCKER_FILE_TEMPLATE = """FROM python:3.6


COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

RUN mkdir /app
COPY DjangoAppCenter.profile.json /app

# 将/app指定为工作目录
WORKDIR /app

EXPOSE 6666

CMD python3 -m DjangoAppCenter deploy

# 使用docker build and run
# docker build -t django.appcenter .
# docker run --restart=always --net=host -d --name django.appcenter django.appcenter
"""
