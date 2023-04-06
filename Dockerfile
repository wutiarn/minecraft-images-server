FROM ubuntu:22.04

RUN apt update && apt install -y --no-install-recommends python3 python3-pip sqlite3

WORKDIR /app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py
