FROM python:3.12.9-alpine3.21

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies
# Most are for phonenumbers library
RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    openssl-dev \
    postgresql-dev

COPY shared/ /app/shared/

COPY web/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    cd /app/shared && \
    pip install -e .

COPY web/ .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]