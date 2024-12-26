# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a directory for the app
WORKDIR /app

# Install dependencies
RUN apk update && apk add gcc python3-dev musl-dev jpeg-dev zlib-dev

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Expose port 5000
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
