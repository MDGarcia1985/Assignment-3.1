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
    FORWARD = 0
    BACKWARD = 1
    RIGHT = 2
    LEFT = 3

@dataclass(frozen=True) #makes it so agents can't mutate results after returning
class StepResult:
    action: Action #this is the action 0-3
    info: Dict[str, object] | None = None
#info is an optional debug metadata (epsilon used, chosen policy, Q values, etc.)
#I like data and debugging
    
class Agent(Protocol):
    """
    Agent is the core abstraction for all AI agents in this project.

    It defines the *contract* that every agent must follow, regardless of
    implementation details (random policy, Q-learning, future planners, etc.).

    The Agent interface answers three fundamental questions:
    1) How does the agent choose an action?        -> act()
    2) How does the agent learn from experience?   -> learn()
    3) How does the agent reset between episodes?  -> reset()

    By programming against this interface, the environment and training
    runner remain completely decoupled from specific learning algorithms.
    This allows different agents to be swapped in and out without changing
    the surrounding system.

    This design supports reuse across multiple unmanned systems projects
    (RC vehicles, UGVs, hybrid platforms, etc.) while keeping learning logic
    isolated and testable.
    """
    name: str
    def reset(self) -> None:
        """Reset any internal state for a new episode"""
        ...
    def act(self, obs: Any) -> StepResult:
        """Choose an action given the current observation."""
        ...

    def learn(
        self, 
        obs: Any, #Observation before the action was take
        action: Action, #Action chosen by the agent at that state
        reward: float, #Rewards are how the AI knows if it did something good or bad. 
                       #It floats because the value is dependent on which model and what action it takes.
        next_obs: Any, #Observation resulting from the action.
        done: bool #Idicates whether the episode has terminated.
    ) -> None:
        """
        Ubdate the agent's internal state based on the transition
        (obs, action, reward, next_obs, done).

        Learning does not return a value; it mutates the agent's
        internal model (Q-table, neural network weights, etc.) in place.
        """
        ...

