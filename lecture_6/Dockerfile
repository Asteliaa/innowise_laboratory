# Base image with Python
FROM python:3.11-slim

# Environment variables for predictable Python behavior
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main application code
COPY main.py .

# Expose port 8000
# This informs Docker that the container listens on port 8000
EXPOSE 8000

# Set the default command to run when the container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
