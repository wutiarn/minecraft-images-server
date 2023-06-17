FROM ubuntu:22.04

COPY files/wkhtmltox_0.12.6.1-2.jammy_amd64.deb /app/files/
RUN apt update && apt install -y --no-install-recommends python3 python3-pip sqlite3 unzip /app/files/wkhtmltox_0.12.6.1-2.jammy_amd64.deb

COPY files/MathJax-2.7.7.zip /app/files/
RUN cd /app/files \
    && unzip MathJax-2.7.7.zip

WORKDIR /app
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD python3 main.py
