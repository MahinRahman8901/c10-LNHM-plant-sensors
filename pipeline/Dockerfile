FROM python:latest

COPY requirements.txt .
COPY plants_data.csv .

RUN pip install -r requirements.txt

COPY load.py .

CMD ["python3", "load.py"]