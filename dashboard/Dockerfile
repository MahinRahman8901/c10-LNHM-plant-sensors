FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN mkdir archived_data

COPY charts.py .

COPY load_from_db.py .

COPY load_from_s3.py .

COPY app.py .

EXPOSE 8051 

CMD ["streamlit", "run", "app.py"]
