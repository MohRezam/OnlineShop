FROM python:latest

WORKDIR /src

COPY requirements.txt .

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src/

EXPOSE 8000 

CMD ["gunicorn", "config.wsgi", ":8000"]
