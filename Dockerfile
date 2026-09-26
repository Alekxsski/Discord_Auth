FROM python:3.14-alpine

WORKDIR /app

COPY backend /app/backend
COPY app.py /app/container
COPY requirements.txt /app
COPY .env /app

RUN pip install --upgrade pip setuptools wheel   
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python" "app.py"]
