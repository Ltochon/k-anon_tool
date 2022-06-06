# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

# switch working directory
WORKDIR /app

ADD . /app
# install the dependencies and packages in the requirements file
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

WORKDIR /app/K-AnoTool

CMD [ "python", "app.py" ]