FROM python:3.13-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y curl git && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Asegurar que Poetry esté en el PATH
ENV PATH="/root/.local/bin:$PATH"

WORKDIR /app

# Copiar archivos de proyecto
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY . .
#TODO: Delete ENV and change structure to do CMD "main.py"
ENV PYTHONPATH=/app/src
EXPOSE 8000
CMD ["poetry", "run", "python", "main.py"]