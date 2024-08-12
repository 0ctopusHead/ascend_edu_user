FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /certs
EXPOSE 5000

CMD ["gunicorn", "-b", ":5000", "--certfile", "/certs/chain.pem", "--keyfile", "/certs/key.pem", "app:app"]
