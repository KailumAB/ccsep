# A sample Makefile to use make command to build, test and run the program
# Guide: https://philpep.org/blog/a-makefile-for-your-dockerfiles/
APP=isec3004.assignment

all: build

build:
	docker build --rm --tag=$(APP) .
	docker image prune -f

test:
	docker run -it --rm $(APP) python manage.py test

run:
	docker-compose pull
	docker-compose build --no-cache db
	docker-compose up -d --force-recreate db
	docker-compose build --no-cache web
	docker-compose up -d --force-recreate web

clean:
	docker-compose down -v
	docker-compose rm
	docker system prune

.PHONY: all test clean
