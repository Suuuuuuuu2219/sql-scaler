from fastapi import FastAPI
from openenv.core.env_server import HTTPEnvServer
from envs.sql_optimizer.env import SQLQueryOptimizerEnv
from envs.sql_optimizer.models import Action, Observation

# 1. Initialize the FastAPI application
app = FastAPI(title="SQL Scaler API")

# 2. Setup the HTTPEnvServer wrapper
server = HTTPEnvServer(
    env=SQLQueryOptimizerEnv,
    action_cls=Action,
    observation_cls=Observation
)

# 3. Explicitly pass "simulation" as a string to resolve internal library conflicts
server.register_routes(app, mode="simulation")

# Run with: PYTHONPATH=. uvicorn server.app:app --host 0.0.0.0 --port 7860
