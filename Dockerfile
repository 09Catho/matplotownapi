FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port
EXPOSE 5150

# Run the application with Gunicorn
# Bind to 0.0.0.0:5150
CMD ["gunicorn", "--bind", "0.0.0.0:5150", "src.app:app"]
