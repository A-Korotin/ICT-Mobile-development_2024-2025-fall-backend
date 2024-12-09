FROM python:3.11

# Установка системных зависимостей для Tesseract OCR и PDF2Image
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    poppler-utils \
    libtesseract-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

#
COPY ./requirements.txt /app/requirements.txt

#
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

#
COPY src /app/src
COPY .env /app/

EXPOSE 8000
#
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]