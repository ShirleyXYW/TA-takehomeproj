FROM python:3.11-slim

WORKDIR /app

RUN pip install prometheus_client

COPY key_server.py .

EXPOSE 1123 8000

CMD ["python", "key_server.py", \
     "--srv-port", "1123", \
     "--max-size", "1024", \
     "--metrics-port", "8000"]