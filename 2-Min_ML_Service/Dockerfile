FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаём папки
RUN mkdir -p data models

EXPOSE 8000 8501

CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000"]