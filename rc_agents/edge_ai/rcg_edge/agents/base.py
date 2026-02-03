"""
base.py

RCG-Edge Base Agent Interface
Defines the common agent interface and base classes for all agents.
All agents (random, Q-learning, etc.) should follow this contract.

Copyright (c) 2026 Michael Garcia, M&E Design
https://mandedesign.studio
michael@mandedesign.studio

CSC370 Spring 2026
"""

from __future__ import annotations

from dataclasses import dataclass #dataclass gives a structured return type for act()
from enum import IntEnum #IntEnum gives us a typed action space
from typing import Any, Dict, Protocol #Any lets obs be flexible without locking in too early
#Dict is for info payloads
#Protocol defines an interface without forcing inheritance

#this is the start of a larger project for UGVs and other unmanned systems.
#Therefore, I used class Action(IntEnum) in order to expand later.
class Action(IntEnum):
    """Discrete action space for grid movement (IntEnum for int compatibility)."""
    FORWARD = 1
    BACKWARD = 2
    RIGHT = 3
    LEFT = 4

@dataclass(frozen=True) #makes it so agents can't mutate results after returning
class StepResult:
    action: Action #this is the action 1-4
    info: Dict[str, object] | None = None
#info is an optional debug metadata (epsilon used, chosen policy, Q values, etc.)
#I like data and debugging
    
class Agent(Protocol):
    name: str
    def reset(self) -> None:
        """Reset any internal state for a new episode"""
        ...
    def act(self, obs: Any) -> StepResult:
        """Choose an action given the current observation."""
        ...

    def learn(
        self, 
        obs: Any, 
        action: Action,
        reward: float,
        next_obs: Any,
        done: bool
    ) -> None:
        """Learn from the last action taken."""
        ...

