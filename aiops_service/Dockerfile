FROM python:3.11-slim

WORKDIR /app
COPY requirements-aiops.txt /app/requirements-aiops.txt
RUN pip install --no-cache-dir -r /app/requirements-aiops.txt
COPY aiops_service /app/aiops_service

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "aiops_service.server:app", "--host", "0.0.0.0", "--port", "8000"]
