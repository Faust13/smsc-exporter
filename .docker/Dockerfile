FROM python:3.11.9-alpine3.19

COPY ./app/requirements.txt /tmp/requirements.txt

RUN pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

COPY ./app/ /app/

WORKDIR /app

EXPOSE 5000

CMD ["python3", "/app/app.py"]


