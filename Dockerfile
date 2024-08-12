FROM python:3.10

WORKDIR /app
COPY . /app


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", ":5000", "--certfile", "/home/root/chain.pem", "--keyfile", "/home/root/key.pem", "app:app"]