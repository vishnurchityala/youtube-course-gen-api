# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the app.py file into the container
COPY app.py app.py

# Install Flask
RUN pip install Flask gunicorn

# Specify the command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
