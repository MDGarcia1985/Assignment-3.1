# Security Bot Training Program - Phase 1: Simple Movement Logging
# By Michael Garcia
# CSC370 Spring 2026
# michael@mandedesign.studio
#
# This is the main program file that coordinates the security bot training
# It imports functions from other modules to keep the code organized
# 
# Phase 1 Focus: Basic movement data collection and logging
# 
# ARCHIVED: This file is preserved for reference but is no longer actively used
# Current development has moved to the rc_agents/ package structure

# # Import the bot control functions from our custom module
# from bot_controller import auto_move_the_robot, manually_move_the_robot

# # Display program introduction and movement key to the user
# # \n creates new lines, \t creates tab indentation for formatting
# print(
#     "\n\n\t*** Training new security bot ***\n"
#     "\tThis program will train a security bot to patrol a warehouse\n"
#     "\tThis bot uses reinforcement learning to build routes and refine patrols\n"
#     "\tThe bot will also show you what it learned\n"
#     "\t1|Forward, 2|Backward, 3|Right, 4|Left\n"
# )

# # ---- Main Program Execution ----
# # This is where the program actually starts running

# # Ask the user which mode they want to use
# # .strip() removes extra spaces, .lower() makes it lowercase
# mode = input("Choose mode: (a)uto or (m)anual? ").strip().lower()

# # Decide which function to run based on user's choice
# # .startswith("a") checks if the input begins with the letter 'a'
# if mode.startswith("a"):
#     # If they chose auto mode, ask how many moves they want
#     moves_input = input("How many moves? (press Enter for 100): ").strip()
#     
#     # If they just pressed Enter (empty string), use default of 100
#     if moves_input == "":
#         moves = 100
#     else:
#         # Convert their input to a number
#         # If they enter something invalid, this will cause an error
#         moves = int(moves_input)
#     
#     # Run automatic training with the specified number of movements
#     auto_move_the_robot(moves)
# else:
#     # For any other input (including 'm' for manual)
#     # Run manual control mode where user types each move
#     manually_move_the_robot()