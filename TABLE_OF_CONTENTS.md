# Table of Contents

This index follows the repository as it exists today and points to the main code, tests, and supporting documents.

## Repository root

- [`README.md`](README.md) - project entry point, run commands, and runner interface notes
- [`ARCHITECTURE.md`](ARCHITECTURE.md) - structural overview of packages, layers, and relationships
- [`pyproject.toml`](pyproject.toml) - Python package metadata and dependencies
- [`pytest.ini`](pytest.ini) - pytest discovery configuration
- [`uv.lock`](uv.lock) - locked dependency graph for `uv`

## Core package: `rc_agents/`

- [`rc_agents/__main__.py`](rc_agents/__main__.py) - CLI smoke-test entry point
- [`rc_agents/README.md`](rc_agents/README.md) - package-level mental model and conventions
- [`rc_agents/config/`](rc_agents/config)
  - [`ui_config.py`](rc_agents/config/ui_config.py) - shared training configuration and converters
- [`rc_agents/envs/`](rc_agents/envs)
  - [`grid_env.py`](rc_agents/envs/grid_env.py) - open grid environment
  - [`maze_env.py`](rc_agents/envs/maze_env.py) - maze environment with walls and reward shaping
- [`rc_agents/edge_ai/rcg_edge/agents/`](rc_agents/edge_ai/rcg_edge/agents)
  - [`base.py`](rc_agents/edge_ai/rcg_edge/agents/base.py) - `Action`, `StepResult`, and agent protocol
  - [`random_agent.py`](rc_agents/edge_ai/rcg_edge/agents/random_agent.py) - random baseline agent
  - [`q_agent.py`](rc_agents/edge_ai/rcg_edge/agents/q_agent.py) - Q-learning agent
  - [`rl_agent.py`](rc_agents/edge_ai/rcg_edge/agents/rl_agent.py) - primary RL agent used by the UI catalog
  - [`rlf_agent.py`](rc_agents/edge_ai/rcg_edge/agents/rlf_agent.py) - exploration-augmented RL agent
- [`rc_agents/edge_ai/rcg_edge/runners/`](rc_agents/edge_ai/rcg_edge/runners)
  - [`train_runner.py`](rc_agents/edge_ai/rcg_edge/runners/train_runner.py) - shared training loop
  - [`maze_runner.py`](rc_agents/edge_ai/rcg_edge/runners/maze_runner.py) - maze generation and maze training helpers
  - [`convergence_tracker.py`](rc_agents/edge_ai/rcg_edge/runners/convergence_tracker.py) - rolling convergence metrics
- [`rc_agents/ui/`](rc_agents/ui)
  - [`app_streamlit.py`](rc_agents/ui/app_streamlit.py) - Streamlit entry point
  - [`gui_main.py`](rc_agents/ui/gui_main.py) - Tkinter-oriented GUI entry
  - [`README.md`](rc_agents/ui/README.md) - UI-specific walkthrough
  - [`streamlit_ui/`](rc_agents/ui/streamlit_ui)
    - [`sidebar_ui.py`](rc_agents/ui/streamlit_ui/sidebar_ui.py) - environment and agent controls
    - [`main_panel.py`](rc_agents/ui/streamlit_ui/main_panel.py) - training flow and result rendering
    - [`factory.py`](rc_agents/ui/streamlit_ui/factory.py) - environment and agent construction
    - [`agent_catalog.py`](rc_agents/ui/streamlit_ui/agent_catalog.py) - declarative UI agent registry
    - [`progressive_learning.py`](rc_agents/ui/streamlit_ui/progressive_learning.py) - session-state reuse and Q-table transfer
  - [`viz/`](rc_agents/ui/viz)
    - [`q_table_viz.py`](rc_agents/ui/viz/q_table_viz.py) - Q-table and value visualizations
    - [`trail_viz.py`](rc_agents/ui/viz/trail_viz.py) - best-run path visualization
- [`rc_agents/utils/logger.py`](rc_agents/utils/logger.py) - execution logging helpers
- [`rc_agents/testers/`](rc_agents/testers) - package test suite for envs, agents, runners, and UI helpers
- [`rc_agents/data/`](rc_agents/data) - saved Q-tables, test artifacts, and training outputs

## Project documentation: `docs/`

- [`docs/PHASE_1.md`](docs/PHASE_1.md) - current-package structure snapshot
- [`docs/PHASE_2.md`](docs/PHASE_2.md) - future target layout for the larger `rc_guardian` direction
- [`docs/DEV_NOTES.md`](docs/DEV_NOTES.md) - implementation notes and working decisions
- [`docs/FOR_BEGINNERS.md`](docs/FOR_BEGINNERS.md) - beginner-facing project explanations
- [`docs/LOGGER_README.md`](docs/LOGGER_README.md) - logging notes
- [`docs/MATH_FOUNDATIONS.md`](docs/MATH_FOUNDATIONS.md) - math background
- [`docs/MARKOV_DECISION_PROCESS.md`](docs/MARKOV_DECISION_PROCESS.md) - reinforcement learning context

## Historical and generated material

- [`archive/`](archive) - earlier prototypes, experiments, and superseded UI files
- [`assignment_3_1.egg-info/`](assignment_3_1.egg-info) - generated packaging metadata
- `__pycache__/`, `.pytest_cache/`, `.venv/` - local runtime and tooling artifacts
