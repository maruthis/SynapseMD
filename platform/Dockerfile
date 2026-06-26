FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir hatchling
COPY pyproject.toml README.md ./
COPY synapsemd_platform ./synapsemd_platform

RUN pip install --no-cache-dir .

EXPOSE 8000
CMD ["uvicorn", "synapsemd_platform.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
