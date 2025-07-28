FROM python:3.10-slim

WORKDIR /app

# Instalar pg_isready que viene con postgresql-client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiar la app y el script de espera
COPY . .

RUN chmod +x /app/wait-for-postgres.sh

# El comando lo sobreescribimos en docker-compose.yml
