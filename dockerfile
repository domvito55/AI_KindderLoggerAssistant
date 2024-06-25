FROM python:3.11

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY service.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]