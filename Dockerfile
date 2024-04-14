FROM python:latest

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/

RUN python manage.py collectstatic --noinput

EXPOSE 8000 

CMD ["gunicorn", "config.wsgi", ":8000"]
