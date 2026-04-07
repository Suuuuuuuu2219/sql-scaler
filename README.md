---
title: SQL Scaler
emoji: 🛡️
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# SQL Scaler 🛡️

SQL Scaler is an OpenEnv-compatible environment designed to train and evaluate AI agents in the art of SQL optimization.

## 🚀 Key Features

-   **3 Difficulty Tasks**: Easy (`SELECT *`), Medium (JOIN aliases), and Hard (Nested subqueries).
-   **Deterministic Grader**: Uses `sqlparse` for strict logic and structural verification.
-   **OpenEnv Native**: Built with the `openenv` framework for seamless agent integration.
-   **AI Baseline**: Includes a baseline inference script using `gpt-4o-mini`.

## 📦 Getting Started

### 1. Installation
```bash
pip install -r requirements.txt
```

### 2. Set API Key (for Baseline)
```bash
export OPENAI_API_KEY="your-api-key"
```

### 3. Run the Server
```bash
uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### 4. Run Baseline Inference
```bash
In a separate terminal:
python baseline/run_baseline.py
```

## 🐋 Docker Development
```bash
docker build -t sql-scaler .
docker run -p 7860:7860 -e OPENAI_API_KEY=$OPENAI_API_KEY sql-scaler
```

## 📊 Environment Specification

-   **Observation**: Current SQL query, table schemas, difficulty, and hints.
-   **Action**: Optimized SQL query string.
-   **Reward**: `0.0` to `1.0` based on correctness and optimization efficiency.
