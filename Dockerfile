# A sample run a Flask program
# Guide: https://blog.bitsrc.io/a-guide-to-docker-multi-stage-builds-206e8f31aeb8
FROM python:3.8.2-alpine as build
MAINTANER Your Name "youremail@domain.tld"

RUN apk --update add build-base 
# Create app directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY src/requirements.txt .
# Install app dependencies
RUN pip install --no-cache-dir --user -r requirements.txt

COPY src .

FROM python:3.8.2-alpine
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP main.py
ENV FLASK_ENV development
# Create app directory
WORKDIR /usr/src/app
COPY --from=build /usr/src/app .
COPY --from=build /root/.local /root/.local
EXPOSE 8080
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0" ]
