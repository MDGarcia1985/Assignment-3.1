# Architecture

This repository is organized around a reusable reinforcement learning core inside `rc_agents/`, with thin entry points for CLI and UI use. The current structure matches the Phase 1 package layout in [`docs/PHASE_1.md`](docs/PHASE_1.md), while [`docs/PHASE_2.md`](docs/PHASE_2.md) provides broader future context for where the project may grow.

## High-level repository structure

```text
NNABL_POC/
├─ README.md
├─ TABLE_OF_CONTENTS.md
├─ ARCHITECTURE.md
├─ pyproject.toml
├─ pytest.ini
├─ uv.lock
├─ docs/
│  ├─ PHASE_1.md
│  ├─ PHASE_2.md
│  ├─ DEV_NOTES.md
│  ├─ FOR_BEGINNERS.md
│  ├─ LOGGER_README.md
│  ├─ MATH_FOUNDATIONS.md
│  └─ MARKOV_DECISION_PROCESS.md
├─ rc_agents/
│  ├─ __main__.py
│  ├─ README.md
│  ├─ config/
│  ├─ data/
│  ├─ edge_ai/
│  ├─ envs/
│  ├─ testers/
│  ├─ ui/
│  └─ utils/
├─ archive/
└─ assignment_3_1.egg-info/
```

## Core system/module breakdown

```text
rc_agents/
├─ __main__.py
├─ config/
│  └─ ui_config.py
├─ envs/
│  ├─ grid_env.py
│  └─ maze_env.py
├─ edge_ai/
│  └─ rcg_edge/
│     ├─ agents/
│     │  ├─ __init__.py
│     │  ├─ base.py
│     │  ├─ random_agent.py
│     │  ├─ q_agent.py
│     │  ├─ rl_agent.py
│     │  └─ rlf_agent.py
│     └─ runners/
│        ├─ __init__.py
│        ├─ convergence_tracker.py
│        ├─ maze_runner.py
│        └─ train_runner.py
├─ ui/
│  ├─ app_streamlit.py
│  ├─ gui_main.py
│  ├─ streamlit_ui/
│  │  ├─ agent_catalog.py
│  │  ├─ coordinates.py
│  │  ├─ factory.py
│  │  ├─ main_panel.py
│  │  ├─ progressive_learning.py
│  │  ├─ safe_eval_num.py
│  │  ├─ sidebar_ui.py
│  │  └─ text_num.py
│  └─ viz/
│     ├─ q_table_viz.py
│     └─ trail_viz.py
├─ testers/
│  ├─ test__action_selection.py
│  ├─ test_agent_catalog.py
│  ├─ test_convergence_tracker.py
│  ├─ test_factory.py
│  ├─ test_grid_env.py
│  ├─ test_maze_env.py
│  ├─ test_maze_generation.py
│  ├─ test_maze_runner.py
│  ├─ test_progressive_learning.py
│  ├─ test_q_update.py
│  ├─ test_random_agent.py
│  ├─ test_rlf_agent.py
│  ├─ test_runtime.py
│  └─ test_trainer.py
└─ utils/
   └─ logger.py
```

## Structural layers

### Entry points

- `README.md` documents the main ways to run the system.
- `rc_agents/__main__.py` is the minimal CLI path for a default training run.
- `rc_agents/ui/app_streamlit.py` is the primary interactive entry point.
- `rc_agents/ui/gui_main.py` preserves a GUI-oriented path outside Streamlit.

These files stay thin and hand off quickly to package modules rather than owning training logic directly.

### Configuration layer

- `rc_agents/config/ui_config.py` defines `TrainingUIConfig` as the shared parameter container.
- The config object converts UI selections into environment and agent-specific config objects.

This keeps episodes, grid size, hyperparameters, and seed values in one place so the CLI, UI, and runner can operate from the same shape of input.

### Environment layer

- `rc_agents/envs/grid_env.py` provides the baseline open-grid world.
- `rc_agents/envs/maze_env.py` extends the same interaction model with walls, reward shaping, and validation.

Both environments are organized around the same `reset()` and `step(action)` contract, which lets the runner stay environment-agnostic.

### Agent layer

- `rc_agents/edge_ai/rcg_edge/agents/base.py` defines the shared action space, `StepResult`, and the protocol agents are expected to follow.
- Concrete agents live beside that contract and vary only in policy and learning behavior.
- `agents/__init__.py` acts as the package export surface for the rest of the system.

The important architectural point is that the runner and UI depend on the agent contract, not on one specific implementation.

### Runner/orchestration layer

- `train_runner.py` is the canonical training loop.
- `maze_runner.py` adds maze-specific setup and generation helpers without duplicating the core episode loop.
- `convergence_tracker.py` records rolling metrics and attaches summaries without changing the training contract.

The runner layer is the boundary where an environment instance, an agent instance, and a shared config object come together.

### UI and visualization layer

- `ui/streamlit_ui/` handles parameter collection, environment and agent selection, session-state reuse, and result presentation.
- `factory.py` translates UI selections into real environment and agent objects.
- `agent_catalog.py` keeps the selectable agents declarative.
- `progressive_learning.py` manages Streamlit reruns by caching agent state and transferring overlapping Q-table knowledge when grid size changes.
- `ui/viz/` renders learned state in table, heatmap, policy, and path forms.

The UI layer depends on the core package, but the core package does not depend on Streamlit-specific concerns.

### Test and artifact layer

- `rc_agents/testers/` mirrors the major functional areas: environments, runners, training behavior, and UI assembly helpers.
- `rc_agents/data/` stores generated learning artifacts and test outputs rather than core source code.
- `archive/` holds prior prototypes and experiments outside the current architecture path.

## How the pieces interact

The common runtime path is:

1. An entry point creates or collects a `TrainingUIConfig`.
2. The UI factory or CLI builds an environment from `rc_agents/envs/`.
3. The UI factory or CLI builds an agent from `rc_agents/edge_ai/rcg_edge/agents/`.
4. `run_training()` in `train_runner.py` coordinates episodes, rewards, learning updates, and convergence tracking.
5. The UI reads the returned results and optional best trajectory, then renders visualizations and summaries.

Maze-specific runs follow the same pattern, but `maze_runner.py` and `factory.py` insert wall generation and maze setup before calling the shared runner.

## Design patterns visible in the codebase

- Contract-first organization: environments and agents are wired through small shared interfaces rather than through one large inheritance tree.
- Thin entry points: `__main__.py` and UI entry files delegate quickly into package modules.
- Factory plus catalog composition: Streamlit selection state is converted into runtime objects through `factory.py` and `agent_catalog.py`.
- Single training loop: `train_runner.py` is treated as the canonical orchestration path instead of duplicating episode logic in each interface.
- Session-backed progressive learning: the Streamlit layer stores long-lived agent instances and selectively transfers learned state across compatible runs.
- Package export boundaries: `__init__.py` files define the import surfaces used by callers.

## Constraints and organizing decisions

- The current repository is centered on the `rc_agents/` package; it is not yet split into the broader multi-package Phase 2 layout.
- The runner intentionally relies on documented behavioral contracts instead of enforcing heavyweight abstract base classes.
- UI modules are designed to be thin and import-safe, with some imports delayed until object construction time.
- `MazeEnv` and `GridEnv` are swappable because they preserve the same `reset()` / `step()` shape.
- Historical code remains in `archive/` instead of being folded into the active package tree.
- Supporting documents in `docs/` are informative context. They explain the current package structure and future direction, but the source tree itself remains the authoritative structure reference.
