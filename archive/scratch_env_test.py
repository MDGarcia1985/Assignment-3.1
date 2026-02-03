from rc_agents.envs.grid_env import GridEnv, GridConfig

env = GridEnv(GridConfig(rows=3, cols=3, start=(0, 0), goal=(2, 2)))

obs = env.reset()
print("Start:", obs)

obs, reward, done, _ = env.step(1)  # forward
print("After forward:", obs, reward, done)

obs, reward, done, _ = env.step(3)  # right
print("After right:", obs, reward, done)

obs, reward, done, _ = env.step(3)  # right
print("After right:", obs, reward, done)

obs, reward, done, _ = env.step(2)  # backward
print("After backward:", obs, reward, done)

obs, reward, done, _ = env.step(2)  # backward
print("After backward:", obs, reward, done)

obs, reward, done, _ = env.step(2)  # backward (should hit row 2)
print("After backward:", obs, reward, done)

obs, reward, done, _ = env.step(3)  # right (if goal is (2,2) this should complete)
print("After right to goal:", obs, reward, done)
