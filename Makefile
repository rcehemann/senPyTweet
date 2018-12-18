export FLASK_APP=app

HOST = 127.0.0.1
PORT = 5000
OPTS = --reload --debugger --lazy-loader --without-threads

install:
	pip3 install -r requirements.txt

help:
	flask run --help

dev:
	FLASK_ENV=development flask run --host $(HOST) --port $(PORT) $(OPTS)

