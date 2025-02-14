FROM python:3.13-slim AS base

WORKDIR /app

COPY . .

COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["python", "gformIMR.py"]
