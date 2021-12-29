FROM python:3.6
ADD . /opt/app
WORKDIR /opt/app
RUN pip install -r requirements.txt
EXPOSE 8003
