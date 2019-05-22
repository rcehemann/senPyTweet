# start from a docker hub python image
FROM python:3.7

# copy requirements
COPY requirements.txt /app/
WORKDIR /app

# install app dependencies
RUN pip3 install -r requirements.txt

# copy entire project
COPY . /app
WORKDIR /app

# start the flask app
ENTRYPOINT ["flask"]
CMD ["run", "--host=0.0.0.0", "--eager-loading", "--with-threads"]

