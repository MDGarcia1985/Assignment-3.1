# Security Bot Training Program - Phase 1: Simple GUI Version
# By Michael Garcia
# CSC370 Spring 2026
# michael@mandedesign.studio
#
# This is a graphical user interface version of the security bot training program
# It uses tkinter (built into Python) to create windows and buttons
#
# Phase 1 Focus: Basic movement data collection with point-and-click interface
#
# ARCHIVED: This file is preserved for reference but is no longer actively used
# Current development has moved to the rc_agents/ package structure

# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import random
# from movement_logger import record_move

# class SecurityBotGUI:
#     def __init__(self):
#         # Create the main window
#         self.root = tk.Tk()
#         self.root.title("Security Bot Training Program")
#         self.root.geometry("400x300")
#         
#         # File for storing movements
#         self.move_file = "data/botmovements.txt"
#         
#         # Create the GUI elements
#         self.create_widgets()
#     
#     def create_widgets(self):
#         # Title label
#         title_label = tk.Label(self.root, text="Security Bot Training Program", 
#                               font=("Arial", 16, "bold"))
#         title_label.pack(pady=10)
#         
#         # Instructions label
#         instructions = tk.Label(self.root, 
#                                text="Train a security bot to patrol a warehouse\n1=Forward, 2=Backward, 3=Right, 4=Left")
#         instructions.pack(pady=10)
#         
#         # Auto mode button
#         auto_button = tk.Button(self.root, text="Auto Mode", 
#                                command=self.auto_mode, 
#                                bg="lightblue", width=15, height=2)
#         auto_button.pack(pady=10)
#         
#         # Manual mode button
#         manual_button = tk.Button(self.root, text="Manual Mode", 
#                                  command=self.manual_mode, 
#                                  bg="lightgreen", width=15, height=2)
#         manual_button.pack(pady=10)
#         
#         # Exit button
#         exit_button = tk.Button(self.root, text="Exit", 
#                                command=self.root.quit, 
#                                bg="lightcoral", width=15, height=2)
#         exit_button.pack(pady=10)
#     
#     def auto_mode(self):
#         # Ask user how many moves (default 100)
#         moves = simpledialog.askinteger("Auto Mode", 
#                                        "How many moves?", 
#                                        initialvalue=100, 
#                                        minvalue=1, 
#                                        maxvalue=1000)
#         
#         if moves is None:  # User clicked Cancel
#             return
#         
#         # Generate random movements
#         for i in range(moves):
#             direction = random.randint(1, 4)
#             record_move(direction, self.move_file)
#         
#         # Show completion message
#         messagebox.showinfo("Auto Mode Complete", 
#                            f"Generated {moves} random movements!\nSaved to {self.move_file}")
#     
#     def manual_mode(self):
#         # Create manual control window
#         manual_window = tk.Toplevel(self.root)
#         manual_window.title("Manual Control")
#         manual_window.geometry("300x250")
#         
#         # Instructions
#         tk.Label(manual_window, text="Click buttons to move the bot:", 
#                 font=("Arial", 12)).pack(pady=10)
#         
#         # Movement buttons
#         tk.Button(manual_window, text="1 - Forward", 
#                  command=lambda: self.manual_move(1), 
#                  bg="yellow", width=12).pack(pady=5)
#         
#         tk.Button(manual_window, text="2 - Backward", 
#                  command=lambda: self.manual_move(2), 
#                  bg="orange", width=12).pack(pady=5)
#         
#         tk.Button(manual_window, text="3 - Right", 
#                  command=lambda: self.manual_move(3), 
#                  bg="pink", width=12).pack(pady=5)
#         
#         tk.Button(manual_window, text="4 - Left", 
#                  command=lambda: self.manual_move(4), 
#                  bg="lightblue", width=12).pack(pady=5)
#         
#         # Close button
#         tk.Button(manual_window, text="Done", 
#                  command=manual_window.destroy, 
#                  bg="lightcoral", width=12).pack(pady=10)
#     
#     def manual_move(self, direction):
#         # Record the movement
#         record_move(direction, self.move_file)
#         
#         # Show confirmation
#         direction_names = {1: "Forward", 2: "Backward", 3: "Right", 4: "Left"}
#         messagebox.showinfo("Movement Recorded", 
#                            f"Bot moved {direction_names[direction]}!\nSaved to {self.move_file}")
#     
#     def run(self):
#         # Start the GUI
#         self.root.mainloop()

# # Create and run the GUI application
# if __name__ == "__main__":
#     app = SecurityBotGUI()
#     app.run()