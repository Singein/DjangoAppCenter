FROM python:3.6

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi
RUN mkdir /app
COPY settings.json /app
WORKDIR /app
EXPOSE 8000
CMD python3 -m DjangoAppCenter deploy
# docker build -t django.appcenter .
# docker run --restart=always --net=host -d --name django.appcenter django.appcenter