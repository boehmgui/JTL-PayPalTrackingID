FROM python:3.8
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt
