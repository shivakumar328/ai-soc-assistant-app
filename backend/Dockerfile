FROM python:3.11-slim

WORKDIR /app

# Install only the core runtime deps for a small, fast image.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

EXPOSE 5000

# Production WSGI server. Override CMD for local debug if needed.
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "app:app"]
