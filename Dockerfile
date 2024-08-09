
FROM python:3.9-slim


WORKDIR /app


RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY summary_output.py /app/summary_output.py
COPY data /data


COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh


RUN chmod +x /usr/local/bin/wait-for-it.sh


CMD ["wait-for-it.sh", "database:3306", "--", "python", "/app/summary_output.py"]
