import random
from typing import Dict, Any, Optional
from openenv.core.env_server.interfaces import Environment
from envs.sql_optimizer.models import Observation, Action, State
from envs.sql_optimizer.tasks import TASKS
from envs.sql_optimizer.grader import grade, normalize

class SQLQueryOptimizerEnv(Environment[Action, Observation, State]):
    def __init__(self):
        super().__init__()
        self._current_task = None
        self._done = False
        self._step_count = 0

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> Observation:
        """Reset the environment to a random task."""
        if seed is not None:
            random.seed(seed)
            
        self._current_task = random.choice(TASKS)
        self._done = False
        self._step_count = 0
        
        return Observation(
            query=self._current_task.query,
            schema=self._current_task.schema_info,
            difficulty=self._current_task.difficulty,
            hint=f"Optimize {self._current_task.difficulty} query",
            done=False,
            reward=None
        )

    def step(
        self,
        action: Action,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> Observation:
        """Process the agent's optimized query and return reward."""
        if not self._current_task:
            raise ValueError("Environment not reset")
            
        if self._done:
            obs = self.state_to_observation()
            obs.reward = 0.0
            return obs
            
        # Compute score using grader
        score = grade(
            original=self._current_task.query,
            predicted=action.optimized_query,
            optimal=self._current_task.optimal
        )
        
        self._done = True
        self._step_count += 1
        
        obs = Observation(
            query=self._current_task.query,
            schema=self._current_task.schema_info,
            difficulty=self._current_task.difficulty,
            hint=f"Goal reached with reward {score}",
            done=self._done,
            reward=score,
            metadata={
                "original": self._current_task.query,
                "optimal": self._current_task.optimal,
                "normalized_predicted": normalize(action.optimized_query)
            }
        )
        return obs

    @property
    def state(self) -> State:
        """Return the current environment state."""
        return State(
            current_query=self._current_task.query if self._current_task else "",
            difficulty=self._current_task.difficulty if self._current_task else "none",
            step_count=self._step_count
        )

    def state_to_observation(self) -> Observation:
        """Helper to convert current state to an observation."""
        if not self._current_task:
            return Observation(
                query="",
                schema={},
                difficulty="none",
                done=False
            )
        return Observation(
            query=self._current_task.query,
            schema=self._current_task.schema_info,
            difficulty=self._current_task.difficulty,
            done=self._done
        )
