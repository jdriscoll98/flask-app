FROM python:3.7.1

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
COPY . /app
WORKDIR /app

ENV FLASK_APP=.
ENV FLASK_ENV=development
ENV FLASK_DEBUG=True

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 5000
RUN flask init-db

ENTRYPOINT [ "flask" ]
CMD ["run"]
