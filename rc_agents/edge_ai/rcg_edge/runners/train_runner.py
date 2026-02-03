"""
train_runner.py

Training Loop Runner
Wires together an environment and an agent, runs episodes, returns metrics.
Coordinates the training process for reinforcement learning agents.

Copyright (c) 2026 Michael Garcia, M&E Design
https://mandedesign.studio
michael@mandedesign.studio

CSC370 Spring 2026
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Protocol

from ..agents.base import Action, StepResult


class Env(Protocol):
    """Minimal env protocol required by the runner."""
    def reset(self) -> Any: ...
    def step(self, action: int) -> tuple[Any, float, bool, Dict[str, object]]: ...


@dataclass
class EpisodeResult:
    episode: int
    steps: int
    total_reward: float
    reached_goal: bool


def run_training(
    env: Env,
    agent: Any,
    episodes: int = 50,
    max_steps: int = 200,
) -> List[EpisodeResult]:
    """Run episodes of interaction between env and agent."""
    results: List[EpisodeResult] = []

    for ep in range(1, episodes + 1):
        obs = env.reset()
        agent.reset()

        total_reward = 0.0
        steps = 0
        done = False

        for _ in range(max_steps):
            steps += 1

            step_result: StepResult = agent.act(obs)
            action: Action = step_result.action  # IntEnum; safe to pass as int

            next_obs, reward, done, info = env.step(int(action))
            total_reward += float(reward)

            agent.learn(
                obs=obs,
                action=action,
                reward=float(reward),
                next_obs=next_obs,
                done=bool(done),
            )

            obs = next_obs
            if done:
                break

        results.append(
            EpisodeResult(
                episode=ep,
                steps=steps,
                total_reward=total_reward,
                reached_goal=done,
            )
        )

    return results
