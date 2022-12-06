FROM python:3.9-slim

WORKDIR /ajapsandal

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=main.py

RUN python -c 'from main import *; db.create_all()'

CMD ["flask", "run", "--host=0.0.0.0"]