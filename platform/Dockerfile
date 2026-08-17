FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir hatchling
COPY pyproject.toml README.md alembic.ini docker-entrypoint.sh ./
COPY synapsemd_platform ./synapsemd_platform
COPY migrations ./migrations
COPY alembic ./alembic

RUN pip install --no-cache-dir . && chmod +x docker-entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["uvicorn", "synapsemd_platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
