install:
	pip3 install -r requirements.txt

dev:
	export FLASK_APP=app
	export FLASK_ENV=development
	flask run

server:
	export FLASK_APP=app
	flask run

