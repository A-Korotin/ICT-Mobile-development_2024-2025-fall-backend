FROM python:3.11
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