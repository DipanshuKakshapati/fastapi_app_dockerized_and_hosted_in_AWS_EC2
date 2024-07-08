FROM python:3.9-slim

# Update and install necessary packages
RUN apt-get update && apt-get upgrade -y \
    && apt-get install -y gnupg2 curl ca-certificates postgresql-client \
    build-essential libpq-dev wget firefox-esr

# Install geckodriver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" -O - | tar -xz -C /usr/local/bin

# Set the working directory in the container
WORKDIR /FAST_API

# Copy the FastAPI application and other necessary files into the Docker container
COPY . /FAST_API

# Install Python dependencies
RUN pip install -r requirements.txt psycopg2-binary aiomysql

RUN pip install sqlalchemy-utils

# Set PYTHONPATH
ENV PYTHONPATH=/FAST_API

# Make port 8000 available to the world outside this container
EXPOSE 8000

# List contents for debugging
RUN ls -la /FAST_API/

# Command to run the Uvicorn server
CMD ["uvicorn", "sql_app.main:app", "--host", "0.0.0.0", "--port", "8000"]

