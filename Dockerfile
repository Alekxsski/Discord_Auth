FROM python:3.14-alpine

RUN apk add --no-cache --update curl ca-certificates openssl git tar bash sqlite fontconfig \
    && adduser --disabled-password --home /home/container container

USER container
ENV  USER=container HOME=/home/container

WORKDIR /home/container

COPY backend /home/container/backend
COPY app.py /home/container
COPY requirements.txt /home/container
COPY .env /home/container

RUN pip install --upgrade pip setuptools wheel   
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python" "app.py"]
