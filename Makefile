export FLASK_APP=app

install:
	pip3 install -r requirements.txt

help:
	flask run --help

dev:
	FLASK_ENV=development flask run --host 127.0.0.1 --port 5000 --reload --debugger --lazy-loader --without-threads

build:
	docker build -t sen-py:latest .

run:
	docker run -p 127.0.0.1:5000:5000/tcp sen-py

prod:
	docker build -t sen-py:latest .
	docker run -d -p 127.0.0.1:5000:5000/tcp sen-py
