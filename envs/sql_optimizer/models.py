from openenv.core.env_server.types import Action as BaseAction, Observation as BaseObservation, State as BaseState
from pydantic import Field
from typing import Optional, Dict, Any

class Observation(BaseObservation):
    query: str
    schema_info: Dict[str, Any] = Field(..., alias="schema")
    difficulty: str
    hint: Optional[str] = None

class Action(BaseAction):
    optimized_query: str

class State(BaseState):
    current_query: str
    difficulty: str
