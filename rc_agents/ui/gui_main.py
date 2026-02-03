"""
gui_main.py

Minimal Tkinter GUI to run training and display results.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk, messagebox

from rc_agents.envs.grid_env import GridEnv, GridConfig
from rc_agents.edge_ai.rcg_edge.agents.q_agent import QAgent, QConfig
from rc_agents.edge_ai.rcg_edge.runners.train_runner import run_training


class TrainerGUI:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("CSC370 Q-Learning Trainer")
        self.root.geometry("520x420")

        self.episodes_var = tk.StringVar(value="50")
        self.max_steps_var = tk.StringVar(value="200")
        self.epsilon_var = tk.StringVar(value="0.10")
        self.alpha_var = tk.StringVar(value="0.50")
        self.gamma_var = tk.StringVar(value="0.90")

        self._build()

    def _build(self) -> None:
        frm = ttk.Frame(self.root, padding=12)
        frm.pack(fill="both", expand=True)

        ttk.Label(frm, text="Training Settings", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        grid = ttk.Frame(frm)
        grid.pack(fill="x", pady=(10, 10))

        def row(label: str, var: tk.StringVar):
            r = ttk.Frame(grid)
            r.pack(fill="x", pady=4)
            ttk.Label(r, text=label, width=14).pack(side="left")
            ttk.Entry(r, textvariable=var, width=12).pack(side="left")

        row("Episodes", self.episodes_var)
        row("Max steps", self.max_steps_var)
        row("Epsilon", self.epsilon_var)
        row("Alpha", self.alpha_var)
        row("Gamma", self.gamma_var)

        ttk.Button(frm, text="Run Training", command=self.run_training_clicked).pack(pady=10)

        ttk.Label(frm, text="Results", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 0))
        self.results_box = tk.Text(frm, height=12, width=60)
        self.results_box.pack(fill="both", expand=True, pady=(6, 0))

    def run_training_clicked(self) -> None:
        try:
            episodes = int(self.episodes_var.get())
            max_steps = int(self.max_steps_var.get())
            epsilon = float(self.epsilon_var.get())
            alpha = float(self.alpha_var.get())
            gamma = float(self.gamma_var.get())
        except ValueError:
            messagebox.showerror("Input error", "Please enter valid numeric values.")
            return

        env = GridEnv(GridConfig(rows=5, cols=5, start=(0, 0), goal=(4, 4)))
        agent = QAgent(QConfig(alpha=alpha, gamma=gamma, epsilon=epsilon), seed=123)

        results = run_training(env=env, agent=agent, episodes=episodes, max_steps=max_steps)

        wins = sum(1 for r in results if r.reached_goal)
        avg_steps = sum(r.steps for r in results) / len(results)
        avg_reward = sum(r.total_reward for r in results) / len(results)

        self.results_box.delete("1.0", tk.END)
        self.results_box.insert(tk.END, f"Episodes: {len(results)}\n")
        self.results_box.insert(tk.END, f"Reached goal: {wins}/{len(results)}\n")
        self.results_box.insert(tk.END, f"Avg steps: {avg_steps:.2f}\n")
        self.results_box.insert(tk.END, f"Avg total reward: {avg_reward:.2f}\n\n")

        # Show last few episodes as a quick sanity view
        self.results_box.insert(tk.END, "Last 10 episodes:\n")
        for r in results[-10:]:
            self.results_box.insert(
                tk.END,
                f"  ep {r.episode:>3}: steps={r.steps:>3} reward={r.total_reward:>6.1f} goal={r.reached_goal}\n",
            )

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    TrainerGUI().run()