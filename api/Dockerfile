FROM python:3.11-slim

WORKDIR /api

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV DB_CONNECT_URL=DB_CONNECT_URL

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080