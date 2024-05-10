FROM python:3.8-slim

WORKDIR /docker_pipeline

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "read_csv_write_to_db.py"]
