FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# docker build -t py-fastapi .
# or
# podman build -t py-fastapi .

# docker run -p 8000:8000 py-fastapi
# or
# podman run -p 8000:8000 py-fastapi