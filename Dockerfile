FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]
