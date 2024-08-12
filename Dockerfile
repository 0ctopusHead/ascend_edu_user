FROM python:3.10

WORKDIR /app
COPY . /app

COPY ascendedu.systems.chained.crt /etc/ssl/certs/ascendedu.systems.chained.crt
COPY ascendedu.systems.key /etc/ssl/private/ascendedu.systems.key

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", ":5000", "--certfile", "/etc/ssl/certs/ascendedu.systems.chained.crt", "--keyfile", "/etc/ssl/private/ascendedu.systems.key", "app:app"]