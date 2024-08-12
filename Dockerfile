FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt


COPY chain.pem /etc/ssl/certs/chain.pem
COPY key.pem /etc/ssl/private/key.pem

EXPOSE 5000

# Use the paths where the certificates are stored in the container
CMD ["gunicorn", "-w", "4", "-b", ":5000", "--certfile", "/etc/ssl/certs/chain.pem", "--keyfile", "/etc/ssl/private/key.pem", "app:app"]
