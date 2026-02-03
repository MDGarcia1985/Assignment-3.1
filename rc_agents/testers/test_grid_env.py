"""
Grid Environment Tester

Phase 1: Basic Movement Control
    By Michael Garcia
    CSC370 Spring 2026
    michael@mandedesign.studio
"""

from rc_agents.envs.grid_env import GridEnv, GridConfig, ACTION_FORWARD

#Function to test the reset function
def test_reset_return_start():
    config = GridConfig(start=(2, 2), goal=(4, 4))
    env = GridEnv(config)
    obs = env.reset()
    assert obs == (2, 2)

#Function to test the step function
def test_forward_at_top_wall_does_not_move():
    env = GridEnv(GridConfig(rows=5, cols=5, start=(0, 2)))
    env.reset()
    obs, reward, done, info = env.step(ACTION_FORWARD)
    assert obs == (0, 2)  # Should not have moved
    assert done is False