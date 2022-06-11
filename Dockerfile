# set base image (host OS)
FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 80
CMD gunicorn --worker-class gevent \
  --workers 2 \
  --bind 0.0.0.0:80 \
  --worker-connections 1000 \
  --timeout 120 \
  patched:app
