FROM python:3.10-slim

WORKDIR /app

COPY ./app /app/app
COPY ./model /app/model
COPY app/requirement.txt .

RUN pip install --upgrade pip
RUN pip install -r requirement.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]