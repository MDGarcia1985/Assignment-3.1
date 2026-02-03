"""
random_agent.py

Baseline Random Agent
Agent that selects actions uniformly at random.
Used to sanity-check the environment and runner before Q-learning.

Copyright (c) 2026 Michael Garcia, M&E Design
https://mandedesign.studio
michael@mandedesign.studio

CSC370 Spring 2026
"""

from __future__ import annotations
 
import numpy as np  # numpy is a standard scientific baseline for ML
from typing import Any

from .base import Action, StepResult

ACTION_VALUES = [a.value for a in Action]

#creat a class of random agent
class RandomAgent:
    """A random agent that selects actions uniformly at random."""
    name = "random"

    def reset(self) -> None:
        # No reset needed for random agent
        pass

    def act(self, obs: Any) -> StepResult:
        """Choose an action uniformly at random"""
        action = Action(np.random.choice(ACTION_VALUES))
        return StepResult(action=action, info={"source": "numpy_rng"})

    def learn(
        self,
        obs: Any,
        action: Action,
        reward: float,
        next_obs: Any,
        done: bool,
    ) -> None:
        """Random agent does not learn."""
        return None