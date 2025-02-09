FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

# Copy test client script
COPY ./compose/local/client/test_client.py /app/test_client.py

CMD ["python", "test_client.py"] 