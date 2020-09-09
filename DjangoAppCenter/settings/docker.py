DOCKER_FILE_TEMPLATE = """FROM python:3.6

RUN mkdir /app



COPY requirements.txt .

RUN pip3 install -r requirements.txt

RUN pip3 install uwsgi

COPY DjangoAppCenter.profile.json /app
# 将/app指定为工作目录
WORKDIR /app

EXPOSE 6666

CMD python3 -m DjangoAppCenter deploy"""
