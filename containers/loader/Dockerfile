FROM python:3.9-slim

WORKDIR /app

COPY /containers/loader/requirement.txt .
COPY /containers/loader/config.yml .

RUN pip install --no-cache-dir -r requirement.txt

COPY src/ /app/src/

CMD ["tail", "-f", "/dev/null"]