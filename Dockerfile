FROM python:3.9

WORKDIR /movielover

COPY . /movielover/

RUN pip install -r requirements.txt

CMD [ "python", "app.py" ]