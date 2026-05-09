# Builder 
FROM python:3.12-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Final image - runtime
FROM python:3.12-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=main.py \
    FLASK_ENV=production


COPY --from=builder /opt/venv /opt/venv

COPY . .

EXPOSE 5000

# Verificar se a aplicação está rodando
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/').getcode() == 200" || exit 1

# Inicializar banco de dados e rodar aplicação
CMD python init_db.py && python main.py