FROM python:3.12-slim

# Evita pyc y buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiar código
COPY src/ /app/

# Exponer puerto Django
EXPOSE 8000

# Modo desarrollo (correcto por ahora)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
