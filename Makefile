export FLASK_APP=app

install:
	pip3 install -r requirements.txt

help:
	flask run --help

dev:
	FLASK_ENV=development flask run --host 127.0.0.1 --port 5000 --reload --debugger --lazy-loader --without-threads

build:
	docker build -t senpytweet:latest .

network:
	docker network create bitfeels

run:
	docker run \
	--network bitfeels \
	--name senpytweet \
	--publish 127.0.0.1:5000:5000/tcp \
	senpytweet:latest

prod:
	docker tag senpytweet:latest thekeele/senpytweet:latest
	docker push thekeele/senpytweet
