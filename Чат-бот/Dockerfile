FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y tesseract-ocr libtesseract-dev poppler-utils unzip tesseract-ocr-kaz && \
    pip install --no-cache-dir --upgrade pip

WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]