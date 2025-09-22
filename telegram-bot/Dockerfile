FROM python:3.11-slim

WORKDIR /telegram-bot

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV TOKEN_TELEGRAM_BOT=TOKEN_TELEGRAM_BOT
ENV DB_CONNECT_URL=DB_CONNECT_URL
ENV CIPHER_KEY=supersecurekey

CMD ["python", "app.py"]