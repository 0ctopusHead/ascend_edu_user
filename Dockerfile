FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN ls -l /certs
EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", ":5000", "--certfile", "/certs/chain.pem", "--keyfile", "/certs/key.pem", "app:app"]
