FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render sets PORT automatically
EXPOSE $PORT

# Run using Gunicorn
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
