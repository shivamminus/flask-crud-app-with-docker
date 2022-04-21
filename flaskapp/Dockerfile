FROM python:3.10.4-slim-buster

WORKDIR /flaskapp

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "app.py"]