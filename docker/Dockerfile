FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY pyproject.toml README.md /app/
COPY src/ /app/src/
COPY tests/ /app/tests/

RUN pip install --upgrade pip setuptools wheel && \
    pip install -e .

CMD ["python", "-m", "self_editing_ai.src.cli", "--goal", "Run default goal"]
