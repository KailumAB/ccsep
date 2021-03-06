# A sample run a Flask program
# Guide: https://blog.bitsrc.io/a-guide-to-docker-multi-stage-builds-206e8f31aeb8
FROM python:3.8.2-alpine as build
MAINTAINER Your Name "youremail@domain.tld"

RUN apk --update add build-base
RUN apk add libffi-dev
RUN apk add openssl-dev
RUN apk add --no-cache libressl-dev musl-dev libffi-dev
# Create app directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY src/requirements.txt .
# Install app dependencies
RUN pip install --no-cache-dir --user -r requirements.txt
RUN pip install alembic

COPY src .

FROM python:3.8.2-alpine
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP vulnerable_app.py
ENV FLASK_ENV development
# Create app directory
WORKDIR /usr/src/app
COPY --from=build /usr/src/app .
COPY --from=build /root/.local /root/.local
EXPOSE 8080
#CMD [ "flask", "db", "upgrade" ]
# add flask, alembic, etc to path
ENV PATH="/root/.local/bin/:${PATH}"
# cd to migrations and run them
WORKDIR /usr/src/app/migrations
#CMD [ "alembic", "upgrade", "head"]
# cd to app and run server
WORKDIR /usr/src/app
#CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0"]
COPY ./boot.sh /boot.sh
RUN chmod +x /boot.sh
ENTRYPOINT ["/boot.sh"]
