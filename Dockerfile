FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if any
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Set PYTHONPATH to root so absolute imports work
ENV PYTHONPATH=/app

# Copy project files
COPY envs/ ./envs/
COPY server/ ./server/
COPY baseline/ ./baseline/
COPY data/ ./data/
COPY openenv.yaml .
COPY README.md .

# Expose port 7860 for Hugging Face Spaces / local
EXPOSE 7860

# Run the FastAPI server
CMD ["uvicorn", "server.app:app", "--host", "0.0.0.0", "--port", "7860"]
