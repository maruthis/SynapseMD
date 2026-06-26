FROM python:3.11-slim

WORKDIR /app

COPY platform/pyproject.toml platform/README.md /app/platform/
COPY platform/synapsemd_platform /app/platform/synapsemd_platform
COPY deploy/openapi-bridge /app/bridge

RUN pip install --no-cache-dir /app/platform && pip install --no-cache-dir -r /app/bridge/requirements.txt

WORKDIR /app/bridge
EXPOSE 8100
CMD ["uvicorn", "bridge:app", "--host", "0.0.0.0", "--port", "8100"]
