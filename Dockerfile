# Base image
FROM python:3.11-slim-bullseye

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Set correct Python path
ENV PYTHONPATH "${PYTHONPATH}:/app/taskmanager"

# Set working directory to project root
WORKDIR /app/taskmanager

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*



# Install system dependencies
RUN apt-get update && \
    apt-get install -y gcc libpq-dev postgresql-client && \
    rm -rf /var/lib/apt/lists/* 

# Create and set work directory
WORKDIR /app/taskmanager

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Add this before collecting static files
# After COPY . .
RUN chmod +x wait-for-db.sh  # Add execute permissions to the script

# Collect static files
RUN python taskmanager/manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "taskmanager.taskmanager.wsgi:application"]
