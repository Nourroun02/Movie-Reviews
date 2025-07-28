FROM python:3.11-slim

# Install system dependencies (kept identical but optimized layer)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    postgresql-client \
    libpq-dev \
    gcc \
    python3-dev \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache (unchanged)
COPY requirements.txt .

# Install Python dependencies (unchanged but added no-warn-script-location)
RUN pip install --upgrade pip --no-warn-script-location && \
    pip install --no-cache-dir -r requirements.txt --no-warn-script-location

# Copy application code (unchanged)
COPY . .

# Run collectstatic remains commented as in original
# RUN python manage.py collectstatic --noinput

# Command remains identical
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]