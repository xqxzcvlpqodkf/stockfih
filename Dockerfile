FROM python:3.11-slim

RUN apt-get update && apt-get install -y stockfish && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir fastapi uvicorn python-chess

RUN ln -s /usr/games/stockfish /usr/local/bin/stockfish || ln -s /usr/bin/stockfish /usr/local/bin/stockfish

WORKDIR /app

COPY main.py .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
