# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies with limited concurrency and disabled progress bar
RUN pip install --no-cache-dir --no-compile --disable-pip-version-check --progress-bar off -r requirements.txt

# Copy the application code into the container
COPY service.py ./

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
