FROM python:3.10-slim

RUN pip install flask yt-dlp

WORKDIR /app
COPY server.py /app/

CMD ["python", "server.py"]