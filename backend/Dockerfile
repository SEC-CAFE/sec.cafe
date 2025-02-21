FROM python:3.8.16

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONIOENCODING=utf-8
ENV PYTHONPATH /app

WORKDIR /app

RUN pip3 config set global.index-url https://mirrors.cloud.tencent.com/pypi/simple/
RUN pip3 config set install.trusted-host mirrors.cloud.tencent.com

COPY requirements.txt /app/requirements.txt
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt

# ADD . /app/