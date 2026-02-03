# Movement Logger Module - Phase 1: Basic File Operations
# By Michael Garcia
# CSC370 Spring 2026
# michael@mandedesign.studio
#
# This module handles saving robot movements to a file
# It can be imported and used by other programs
#
# Phase 1 Focus: Simple text file logging for movement data
#
# ARCHIVED: This file is preserved for reference but is no longer actively used
# Current development has moved to the rc_agents/ package structure

# def record_move(direction_number: int, filename: str = "data/botmovements.txt") -> None:
#     """Append one move to the movement log.
#     
#     This function takes a number and saves it to a text file.
#     Each movement gets written on its own line.
#     
#     Args:
#         direction_number: Integer 1-4 representing movement direction
#                          (1=Forward, 2=Backward, 3=Right, 4=Left)
#         filename: Name of file to save to (default: "botmovements.txt")
#     
#     -> None means this function doesn't return any value back
#     """
#     # Open the file in "append" mode ("a") so we don't erase existing data
#     # "with open" automatically closes the file when we're done
#     # encoding="utf-8" ensures text is saved properly
#     with open(filename, "a", encoding="utf-8") as file:
#         # Write the direction number followed by a newline (\n)
#         # f"{direction_number}" puts the variable inside the string
#         file.write(f"{direction_number}\n")