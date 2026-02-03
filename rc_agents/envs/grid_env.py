"""
grid_env.py

Minimal grid environment for reinforcement learning training.
Configurable 2D grid world for navigation tasks.

Copyright (c) 2026 Michael Garcia, M&E Design
https://mandedesign.studio
michael@mandedesign.studio

CSC370 Spring 2026

Actions: 
    1 = FORWARD (up)
    2 = BACKWARD (down)
    3 = RIGHT
    4 = LEFT
"""

# Naming convetion note:
# - CamelCase for classes and type aliases
# - snake_case for functions and variables
# - ALL_CAPS for constants
# The mixing reflects different semantic roles

from __future__ import annotations

from dataclasses import dataclass # @dataclass is a container for env config/state
from typing import Dict, Tuple # typing hints for dictionaries and tuple

import random # randomly determined sample from a probability distribution

# Use built-in min/max instead of numpy for simple clipping
# This removes the numpy dependency for this basic grid environment

ACTION_FORWARD = 1
ACTION_BACKWARD = 2
ACTION_RIGHT = 3
ACTION_LEFT = 4

#valid_actions tells the runner what actions it can accept
VALID_ACTIONS = (
    ACTION_FORWARD,
    ACTION_BACKWARD,
    ACTION_RIGHT,
    ACTION_LEFT,
)

Obs = Tuple[int, int] # observation type (row, col)
StepReturn = Tuple[Obs, float, bool, Dict[str, object]]

@dataclass # dataclass automatically generates boilerplate like __init__, __repr__, etc
class GridConfig:
    rows: int = 5 #simple container for grid settings
    cols: int = 5 #default 5x5 grid
    start: Obs = (0, 0) #initial (row, col) position (default top-left corner)
    goal: Obs = (4, 4) #Default target

class GridEnv: #defines env object
    def __init__(self, config: GridConfig | None = None): # sets up the env, config: GridConfig lets you pass a config or use defaults
        self.config = config if config is not None else GridConfig() # stores config.
        self.pos: Obs = self.config.start # stores current position. Initialize to start.
    
    def reset(self) -> Obs: # returns to start position
        self.pos = self.config.start
        return self.pos

    def step(self, action: int) -> StepReturn:
        """Apply an action to the environment and return the result."""
        if action not in VALID_ACTIONS:
            raise ValueError(f"Invalid action {action}")
        
        # unpack current position
        row, col = self.pos

        # compute new position based on action
        if action == ACTION_FORWARD:
            row -= 1
        elif action == ACTION_BACKWARD:
            row += 1
        elif action == ACTION_RIGHT:
            col += 1
        elif action == ACTION_LEFT:
            col -= 1

        # clip new position to grid boundaries using built-in min/max
        row = max(0, min(row, self.config.rows - 1))
        col = max(0, min(col, self.config.cols - 1))

        # update position
        self.pos = (row, col)

        # compute reward
        reward = -1.0 # default reward is -1 for each move
        done = False # default state is not done

        # check for goal
        if self.pos == self.config.goal:
            reward = 0.0 # reward is 0 if you reach the goal
            done = True # done is true if you reach the goal

        info: Dict[str, object] = {"pos": self.pos} # info is a dictionary for additional info (empty for now)
        return self.pos, reward, done, info
