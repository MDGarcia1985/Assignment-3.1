# Bot Controller Module - Phase 1: Basic Movement Control
# By Michael Garcia
# CSC370 Spring 2026
# michael@mandedesign.studio
#
# This module contains the robot movement control functions
# It handles both automatic and manual movement modes
#
# Phase 1 Focus: Simple movement generation and logging
#
# ARCHIVED: This file is preserved for reference but is no longer actively used
# Current development has moved to the rc_agents/ package structure

# # Import the random module to generate random numbers for automatic movement
# import random
# # Import our custom movement logger function from the other file
# from movement_logger import record_move

# # Create a constant (variable that doesn't change) for the filename
# # This makes it easy to change the filename later if needed
# MOVE_FILE = "data/botmovements.txt"


# def auto_move_the_robot(moves: int = 100) -> None:
#     """Generate random movements for bot training.
#     
#     This function simulates the robot moving on its own.
#     It picks random directions and saves each one.
#     
#     Args:
#         moves: Number of random movements to generate (default: 100)
#                The "= 100" means if no number is given, use 100
#     
#     -> None means this function doesn't return any value back
#     """
#     # Print status messages to let user know what's happening
#     print("\n\t*** Training in progress ***\n")
#     print(f"I am about to move {moves} times on my own and record that movement.\n")

#     # Loop from 1 to the number of moves (inclusive)
#     # range(1, moves + 1) creates numbers 1, 2, 3... up to moves
#     for i in range(1, moves + 1):
#         # Generate a random integer between 1 and 4 (inclusive)
#         # This represents one of the four movement directions
#         direction_number = random.randint(1, 4)

#         # Show the user what move we're on and which direction was chosen
#         print(f"On move {i} of {moves}")
#         print(f"Bot has moved {direction_number}")

#         # Call our imported function to save this movement to the file
#         record_move(direction_number, MOVE_FILE)

#     # Let the user know we're finished
#     print(f"\nDone. Movement history saved to '{MOVE_FILE}' in this folder.\n")


# def manually_move_the_robot() -> None:
#     """Allow user to manually control bot movements.
#     
#     This function lets the user type in directions for the robot.
#     It keeps asking for input until the user types 'q' to quit.
#     It also checks that the input is valid (1, 2, 3, 4, or q).
#     
#     -> None means this function doesn't return any value back
#     """
#     # Print instructions for the user
#     print("\n\t*** Manual control ***\n")
#     print("Enter 1-4 to move, or 'q' to quit.\n")

#     # Start an infinite loop - it will only stop when we use 'break'
#     while True:
#         # Get input from user and clean it up:
#         # .strip() removes extra spaces at beginning/end
#         # .lower() converts to lowercase so 'Q' becomes 'q'
#         user_in = input("Next move (1-4) or q: ").strip().lower()

#         # Check if user wants to quit (accepts q, quit, or exit)
#         if user_in in ("q", "quit", "exit"):
#             print(f"\nExiting. Movement history saved to '{MOVE_FILE}'.\n")
#             break  # This exits the while loop

#         # Check if the input is a valid movement (must be 1, 2, 3, or 4)
#         if user_in not in ("1", "2", "3", "4"):
#             print("Please enter 1, 2, 3, 4, or q.")
#             continue  # This skips the rest and goes back to the top of the loop

#         # Convert the string input to an integer number
#         # We know it's safe because we already validated it above
#         direction_number = int(user_in)

#         # Show the user what happened and save the movement
#         print(f"Bot has moved {direction_number}")
#         record_move(direction_number, MOVE_FILE)