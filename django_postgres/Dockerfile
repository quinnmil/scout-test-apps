FROM python:3.11-bookworm
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev
RUN mkdir /app

WORKDIR /app

ADD requirements.txt /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]