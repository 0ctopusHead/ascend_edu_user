FROM python:3.11-alpine
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80
CMD ["gunicorn", "-b", "0.0.0.0:80", "app:app"]