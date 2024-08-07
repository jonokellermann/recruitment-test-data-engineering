FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY helper_funcs.py .
COPY people_schema.sql .
COPY places_schema.sql .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
