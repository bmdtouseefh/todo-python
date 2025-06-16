# Dockerfile
# Use a slim Python base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your app will run on
EXPOSE 8000

# Command to run the application (can also be specified in docker-compose.yml)
# CMD ["python", "main.py"]

