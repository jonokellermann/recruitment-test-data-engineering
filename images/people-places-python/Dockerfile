FROM python:3.10

WORKDIR /app

COPY requirements.txt .
COPY main.py .
COPY helper_funcs.py .
COPY dataframes.py .
COPY schemas/ .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "main.py"]
