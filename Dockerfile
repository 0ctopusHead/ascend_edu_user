FROM python:3.10

ENV GROUP_ID=1000 \
    USER_ID=1000

WORKDIR /var/www
COPY . /var/www


RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:create_app()"]