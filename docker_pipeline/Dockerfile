FROM python:3.8-slim

WORKDIR /docker_pipeline

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "data_ingestion.py"]
