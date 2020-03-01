FROM python:3.8-alpine3.11

RUN mkdir /test

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /test
COPY test_* .

COPY entrypoint.sh .
RUN command chmod +x entrypoint.sh

ENTRYPOINT [ "./entrypoint.sh" ]
