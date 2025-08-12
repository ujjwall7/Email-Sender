# slim-buster is an operating system to add this file

FROM python:3.8-slim-buster

WORKDIR /mail_sender  # any name

COPY req.txt req.txt

RUN pip install -r req.txt

COPY . .

EXPOSE 8000

CMD python manage.py runserver