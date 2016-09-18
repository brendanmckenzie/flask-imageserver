FROM tiangolo/uwsgi-nginx-flask:flask

COPY ./ /app/

RUN ["pip", "install", "-r", "/app/requirements.txt"]
