FROM python:3.11

WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt ./

# Install dependencies with pip upgrade and retry logic
RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt || \
  (sleep 5 && pip install --no-cache-dir -r requirements.txt)

# Copy the application code into the container
COPY service.py ./

# Expose port 8000 to the outside world
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
