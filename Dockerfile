FROM ubuntu:16.04
COPY CardboardCube/ /cardboardcube

RUN apt-get update
RUN apt-get install -y python3-dev mysql-client libmysqlclient-dev python3-pip
RUN pip3 install -r /cardboardcube/requirements.txt

EXPOSE 80
WORKDIR /cardboardcube
CMD ["sh", "-c", "$STARTUP_COMMAND"]
