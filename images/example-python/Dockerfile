FROM python:3.9-slim

WORKDIR /app

COPY ./load_data.py /app/load_data.py
COPY ./data /data

COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh

RUN pip install mysql-connector-python pandas

CMD ["wait-for-it.sh", "database:3306", "--", "python", "/app/load_data.py"]
