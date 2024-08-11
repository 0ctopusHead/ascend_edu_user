FROM python:3.10

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000
ENV FLASK_APP=app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]