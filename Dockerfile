# Imagem enxuta e com boas práticas: base slim, usuário não-root, healthcheck.
FROM python:3.10-slim

# Não gerar .pyc e não bufferizar stdout (logs aparecem na hora no container).
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copiar só o requirements primeiro aproveita o cache de camadas do Docker:
# enquanto as deps não mudam, o layer de install é reaproveitado entre builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# Rodar como usuário sem privilégios reduz o impacto de uma eventual exploração.
RUN useradd --create-home --uid 1000 appuser
USER appuser

EXPOSE 8000

# Healthcheck no nível da imagem: orquestradores (compose/k8s) sabem quando o container está pronto.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://localhost:8000/health').status==200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
