FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt .
ARG API_VERSION=v1.0.0
ENV API_VERSION=$API_VERSION
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

