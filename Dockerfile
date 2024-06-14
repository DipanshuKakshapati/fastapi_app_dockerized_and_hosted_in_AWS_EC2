# Use an official Python runtime as a parent image, Debian-based, with platform specification for amd64

FROM --platform=linux/amd64 python:3.9-slim

# Update and upgrade the system
RUN apt-get update && apt-get upgrade -y && apt-get dist-upgrade -y

# Install necessary packages
RUN apt-get install -y gnupg2 curl apt-transport-https ca-certificates

# Install build tools (gcc, g++, make)
# These might still be necessary if any Python packages require compilation
RUN apt-get install -y build-essential

# Download and install geckodriver for Firefox if you're using it for scraping or automated tasks
RUN curl -L "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" | tar -xz -C /usr/local/bin

# Install Firefox ESR if it's still required for your application
RUN apt-get install -y firefox-esr

# Set the working directory in the container
WORKDIR /FAST_API

# Copy the FastAPI application and other necessary files into the Docker container
COPY . /FAST_API

# Install any needed packages specified in requirements.txt and aiomysql for async support
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install aiomysql

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Command to run the Uvicorn server
CMD ["uvicorn", "sql_app.main:app", "--host", "0.0.0.0", "--port", "8000"]
