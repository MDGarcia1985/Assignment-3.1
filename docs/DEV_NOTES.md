## RC Agents - Development Notes & Architecture Reference

Author: Michael Garcia  
CSC370 Spring 2026  
M&E Design  
https://mandedesign.studio

## Context

This document exists to capture design intent, architectural patterns, and "why" decisions that are easy to forget over time.

This document is:

- A developer-facing internal reference
- A place to preserve design reasoning
- A bridge between the current project and future robotics platforms

This document is not:

- User documentation
- Grading documentation
- A polished product overview

It is a reference for future development across:

- `rc_guardian`
- Propane hybrid UGV
- Lawn care / snow removal platforms
- Simulation + real hardware parity

If something looks "obvious" today, it will not be in six months. Write it down.

## Core Principles

### Package Philosophy

This project is designed as a long-lived, modular robotics codebase, not a single assignment.

Core principles:

- Clear separation of environment, agent, runner, and UI
- No monolithic scripts
- Same agents must work in:
  - CLI
  - Tkinter GUI
  - Streamlit UI
  - Headless / embedded execution
- Environments should be swappable:
  - Grid
  - Yard
  - Real sensors

### Design Guardrails

Do not:

- Put learning logic in UI
- Put logging configuration in agents
- Allow agents to control the training loop
- Couple environment physics to agent internals

Always:

- Keep agents stateless between episodes except Q-table state
- Keep exploration swappable
- Keep evaluation measurable

### Tests Philosophy

Tests are behavioral, not cosmetic.

They answer:

- Did the agent choose the correct action?
- Did Q-values update correctly?
- Did terminal logic behave as expected?

Tests are intentionally small and focused.

- Passing tests = system integrity
- Failing tests = design signal, not noise

### Human-Readable Code

This codebase is written for humans first.

Comments should:

- Explain intent
- Explain tradeoffs
- Explain "why", not just "what"

Minor typos in comments are acceptable. Opaque code is not.

## System Architecture

### High-Level Structure

```text
rc_agents/
├─ envs/
├─ edge_ai/
│  └─ rcg_edge/
│     ├─ agents/
│     └─ runners/
├─ utils/
├─ config/
└─ ui/
```

The project is intentionally organized so that agents, environments, runners, UI, and utilities remain separable and reusable.

### Agents

#### Base Contract

`Agent` defines the minimum contract for all agents:

- `reset()`
- `act(obs)`
- `learn(obs, action, reward, next_obs, done)`

Agents do not control the loop. They only react to observations and feedback.

This allows:

- Random agents
- Q-learning agents
- Future planners
- Hardware-driven agents

All are interchangeable as long as they follow the same contract.

#### Structural Notes

```text
edge_ai/
└─ rcg_edge/
   └─ agents/
      ├─ base.py
      ├─ random_agent.py
      ├─ q_agent.py
      ├─ rl_agent.py
      └─ rlf_agent.py
```

### Environments

`GridEnv` is intentionally minimal:

- Deterministic movement
- Bounded grid
- Explicit reward shaping

Reward model:

```python
reward = -1.0  # every step costs something
```

Design intent:

- Penalize long paths
- Encourage efficiency
- Reaching the goal stops the penalty (`reward = 0`)

The agent learns to minimize total negative reward, not chase positive reinforcement.

This mirrors real constraints:

- Energy usage
- Time cost
- Wear on hardware

### Runners

Runners own orchestration.

- Agents do not run themselves
- UI does not run learning logic
- Runners coordinate episodes, metrics, and evaluation

Tournament-style comparative evaluation is also a runner concern, not an agent concern.

#### Structural Notes

```text
edge_ai/
└─ rcg_edge/
   └─ runners/
      ├─ train_runner.py
      ├─ maze_runner.py
      └─ convergence_tracker.py
```

### UI

UI strategy:

- Tkinter = assignment compliance + local debugging
- Streamlit = visualization + parameter tuning

UI does not contain logic.

UI populates config, then the runner executes.

No training logic should ever live in UI files.

#### Streamlit UI Structure

Decision intent: one place to choose environment and agents, run training, and compare results without duplicating runner logic.

```text
ui/
├─ app_streamlit.py
├─ gui_main.py
├─ streamlit_ui/
│  ├─ sidebar_ui.py
│  ├─ main_panel.py
│  ├─ factory.py
│  ├─ agent_catalog.py
│  └─ progressive_learning.py
└─ viz/
   ├─ q_table_viz.py
   └─ trail_viz.py
```

#### Streamlit UI Responsibilities

`sidebar_ui.py`

- Environment dropdown (`Open World`, `Maze`) from `factory.get_env_options()`
- Agent checkboxes built from `agent_catalog`
- Hyperparameters:
  - episodes
  - max steps
  - alpha
  - gamma
  - epsilon
- Grid size and start / goal
- `Reset Agents` clears cached agents so the next run starts fresh
- `Save / Load` offers download / upload of a learned Q-table (`.npz`) for agents that support `to_bytes` / `from_bytes`

`main_panel.py`

- `Run Training` builds env via `factory.make_env(cfg, game_type)`
- For each selected agent:
  - reuse cached agent when `agent_key` and grid match
  - transfer Q-table when key matches but grid size changed
  - create a new agent otherwise
- `run_training(env, agent, cfg)` returns `(results, best_trajectory)`
- Each agent gets an expandable section:
  - summary
  - Q-table
  - value heatmap
  - policy
- `Best run (trail)` uses `best_trajectory` and `env.walls` when present

`progressive_learning.py`

- `agent_store`, `agent_key_store`, and `agent_grid_store` keyed by `agent_id` keep per-agent state across reruns
- `agent_key(cfg)` is:

```python
(alpha, gamma, epsilon, seed)
```

- When key and grid match, the same agent is reused
- When only the grid changes, `transfer_q_table(old_agent, new_agent, rows, cols)` copies overlapping Q-values so learning is preserved when resizing the environment

`factory.py`

- `make_agent(agent_id, cfg)` and `make_env(cfg, game_type)` centralize construction so the UI stays thin
- `get_env_options()` returns the list of `(value, label)` for the environment dropdown
- Heavy imports live inside factory functions to avoid import-time failures when adding new agents or environments

### Logging

Execution logging exists for:

- Debugging
- Replay
- Accountability

This will later support:

- Field logs
- Safety audits
- Failure analysis

Logging is centralized at application entry points.

Modules define loggers:

```python
logger = logging.getLogger(__name__)
```

Only entry points configure logging:

```python
if not logging.getLogger().hasHandlers():
    logging.basicConfig(...)
```

Why:

- Prevent duplicate handlers
- Maintain framework compatibility (`Streamlit`, CLI)
- Preserve clean separation of concerns

Agents never configure logging.

This ensures portability to:

- Embedded systems
- Headless deployments
- Field logging
- Hardware safety audits

## Implementation Patterns

### Dataclasses

#### Rule

Use `dataclass` for:

- Training configuration
- UI configuration
- Environment configuration
- Step / result containers

#### Why

- Self-documenting parameters
- Safe defaults
- Easy UI binding (`Tkinter`, `Streamlit`)
- Serializable later (`JSON`, `YAML`)
- Cleaner diffs when values change

This is preferred over long positional argument lists.

#### Example

Typical uses include:

- Training config containers
- Environment config containers
- Result / step containers

### Relative Imports

#### Rule

- If the file lives inside `rc_agents/`, use relative imports
- Only `__main__.py` or Streamlit entry points should use absolute imports
- If you need more than two `..`, reconsider the module location

#### Why

This project uses explicit relative imports to keep modules portable and refactor-safe.

Mental model:

- Relative imports move through the package tree, not the filesystem

#### Reference Tree

```text
rc_agents/
├─ envs/
├─ edge_ai/
│  └─ rcg_edge/
│     ├─ agents/
│     └─ runners/
├─ utils/
└─ config/
```

#### Relative Import Mapping

| Relative Import | Resolves To |
| --- | --- |
| `.` | current package |
| `..` | parent package |
| `..envs` | `rc_agents.envs` |
| `..utils` | `rc_agents.utils` |
| `..config` | `rc_agents.config` |
| `..edge_ai` | `rc_agents.edge_ai` |
| `..edge_ai.rcg_edge.agents` | `rc_agents.edge_ai.rcg_edge.agents` |

#### Example

Importing the grid environment:

```python
from ..envs import GridEnv, GridConfig
```

Equivalent absolute import:

```python
from rc_agents.envs import GridEnv, GridConfig
```

Importing the Q-agent:

```python
from ..edge_ai.rcg_edge.agents import QAgent, QConfig
```

### Module Boundaries

#### Rule

- Agents define behavior
- Environments define transition and reward dynamics
- Runners define orchestration
- UI defines interaction and visualization
- Logging configuration belongs at entry points

#### Why

Module boundaries are what keep this codebase reusable across:

- CLI
- Tkinter GUI
- Streamlit UI
- Headless / embedded execution
- Future robotics platforms

#### Example

- `GridEnv` and future environments should be swappable
- UI should populate config and then call runners
- Agents should be interchangeable under the same contract

### Logging Pattern

#### Rule

- Modules may create loggers
- Modules do not configure global logging
- Entry points configure logging once

#### Why

- Prevent duplicate handlers
- Avoid framework conflicts
- Keep agents and core logic portable

#### Example

Module-level logger:

```python
logger = logging.getLogger(__name__)
```

Entry-point configuration:

```python
if not logging.getLogger().hasHandlers():
    logging.basicConfig(...)
```

## Agent Models & Strategies

### Random

Purpose:

- Baseline behavior
- Sanity checking
- Debugging environments

It does not learn.

It defines what is possible, not what is optimal.

### Q-learning

Purpose:

- First learning agent
- Memory-based decision making
- Baseline for all future RL extensions

Key traits:

- Uses epsilon-greedy policy
- Stores values in a Q-table
- Learns only from non-terminal states

#### Terminal vs Non-Terminal States

Terminal state:

- Episode is over
- No future reward possible
- Learning target = immediate reward only

Non-terminal state:

- Episode continues
- Future rewards still possible
- Learning target includes discounted future value

This distinction prevents the agent from hallucinating future rewards after an episode ends.

### RLF (Fractal)

Purpose:

- Q-learning plus fractal-driven exploration
- Structured alternative to classic epsilon-greedy random exploration

RLF should be treated as a comparable exploration strategy, not as mysticism or branding.

### GA / MANDO Concepts

#### Agent_GA

Purpose:

- Genetic algorithm policy search

This uses a different learning loop, but can still be treated as "an agent" in the broader evaluation framework.

#### Agent_MANDO

Purpose:

- Mandelbrot-parameterized explorer
- Or meta-controller that mutates `c`

Future direction:

- Instead of fixing parameter `c`, allow it to evolve

Two approaches:

- Deterministic schedule across Mandelbrot parameter space
- Error-correcting mutation (Reed-Solomon-inspired constraints)
- Fitness-weighted parameter mutation

Conceptually:

- `RLF` = Julia dynamics at fixed `c`
- `MANDO` = exploration across Mandelbrot space of `c`

This becomes meta-learning over exploration patterns.

## Exploration Strategy (Fractal / Math)

### Motivation

Classic epsilon-greedy exploration samples uniformly at random.

That works, but:

- It has no structure
- It has no memory
- It does not scale well as state space grows

RLF introduces deterministic-chaotic exploration via Julia dynamics:

```text
z_(n+1) = z_n^2 + c
```

The complex state is mapped to:

```text
theta = atan2(Im(z), Re(z))
```

Which is normalized to:

```text
theta in [0, 2pi)
```

This continuous heading is then softly projected onto discrete actions.

### Mechanism

Fractal exploration generates a continuous heading from Julia dynamics, then converts that heading into action probabilities over the discrete action space.

### Action Mapping

Current environment supports 4 actions:

- `FORWARD`
- `BACKWARD`
- `LEFT`
- `RIGHT`

Mapping strategy:

- Compute angular distance to each action heading
- Convert distance to weight via:

```text
w = exp(-kappa * d^2)
```

- Normalize:

```text
p = w / sum(w)
```

- Sample action from `p`

This preserves compatibility with `GridEnv` while enabling future expansion.

### Movement Stub (Future Expansion)

The `_ACTION_DELTAS` structure exists to support:

- 8-direction movement
- Continuous headings
- Hardware-aligned motion (wheel velocity mapping)

Movement logic will eventually migrate from `GridEnv` into a more general motion model.

Current stub is intentionally isolated.

### Why It Matters

Uniform random exploration treats space as flat.

Fractal exploration:

- Produces structured coverage
- Creates non-repeating exploration sequences
- Avoids purely memoryless action sampling
- Introduces tunable chaos via parameter `c`

This creates a middle ground between:

- Random noise
- Fully deterministic planners

Fractal ideas are not the goal.

Measurable improvement is the goal.

## Evaluation Framework

### Tournament Structure

To explore different trainers with quantifiable results:

- `Agent_RL` = Q-learning + classic epsilon-greedy random explore
- `Agent_RLF` = Q-learning + fractal-driven exploration
- `Agent_GA` = genetic algorithm policy search
- `Agent_MANDO` = Mandelbrot-parameterized explorer or meta-controller

Tournament runner pattern:

- Creates env per agent run
- Reuses same config + seeds
- Stores `(agent_name -> results + artifacts)`

Pseudo-structure:

```python
AGENTS = {
    "RL": lambda: QAgent(...classic...),
    "RLF": lambda: QAgent(...fractal explore...),
    "GA": lambda: GAAgent(...),
    "MANDO": lambda: MandoAgent(...),
}

scoreboard = []
details = {}

for name, make_agent in AGENTS.items():
    agent = make_agent()
    env = GridEnv(cfg.to_grid_config())
    results, best_trajectory = run_training(env, agent, cfg)

    wins = sum(r.reached_goal for r in results)
    avg_steps = sum(r.steps for r in results) / len(results)
    scoreboard.append({...})
    details[name] = {"agent": agent, "results": results}
```

### Metrics

Agents should not be evaluated emotionally.

They should be evaluated comparatively.

Use the same:

- Environment
- Seed
- Config
- Independent agent instances

Metrics:

- Win rate
- Average steps to goal
- Convergence slope
- Q-table entropy
- Exploration diversity

This enables:

- RL vs RLF comparison
- RLF vs GA
- MANDO vs all baselines

Comparisons must be apples-to-apples.

### Experimental Discipline

Before adding new math:

- Define measurable hypothesis
- Define control agent
- Define metric
- Run multiple seeds
- Log results

Checklist:

- [ ] Hypothesis is explicit
- [ ] Baseline agent is defined
- [ ] Metrics are chosen before the run
- [ ] Multiple seeds are used
- [ ] Results are logged
- [ ] Comparisons are apples-to-apples

## Hardware & Real-World Constraints

### Hardware Parity Considerations

`GridEnv` is a controlled abstraction.

Real hardware introduces:

- Sensor noise
- Actuator lag
- Energy constraints
- Safety bounds

### Non-Negotiable Rules

Exploration strategies must remain:

- Bounded
- Recoverable
- Interruptible

Fractal exploration is acceptable only if:

- Action deltas remain bounded
- Fail-safe termination exists
- Logging captures trajectory

This is non-negotiable in UGV deployments.

### Safety and Traceability Rules

- Logging must support replay and accountability
- Behavior must remain bounded under exploration
- Systems must support interruption and fail-safe termination
- Real-world deployment requires auditability, not just task success

## Long-Term Direction

This project is converging toward:

- Unified simulation + hardware stack
- Swappable exploration strategies
- Structured experiment harness
- Reproducible learning experiments
- Fractal / GA / classical RL coexistence

This is not an assignment.

This is an extensible robotics learning framework.
