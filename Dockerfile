FROM python:3.8-alpine
RUN apk add --update --no-cache \
    py-pip build-base  linux-headers libxslt-dev
RUN mkdir /app

COPY requirements.txt /app
WORKDIR /app
RUN python -m pip install -r requirements.txt  \
&& apk del build-base linux-headers py-pip \
&& apk add libpq && rm -rf /var/cache/apk/* \
&& find / -name "*.pyc" -delete && find / -name "*.o" -delete

COPY source/ /app

CMD ["python3", "/app/main.py","-c", "/app/config.ini"]
