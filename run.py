"""
Module: lock_cracker_game

This module contains functions related to the Lock Cracker game.
"""
import os
import random
import time
from colorama import init, Fore, Back, Style
import gspread
from google.oauth2.service_account import Credentials

init()
# Google Sheets credentials and API setup
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
# Open the specific spreadsheet
SPREADSHEET = 'save_waldo'
SHEET = GSPREAD_CLIENT.open(SPREADSHEET)
# Specify the worksheet to use
WORKSHEET_NAME = 'players'
worksheet = SHEET.worksheet(WORKSHEET_NAME)


# Inputs related functions
def input_for_saving_info(prompt):
    """
    Prompt the user for input with a green background.

    Parameters:
    - prompt (str): The prompt message to display to the user.

    Returns:
    - str: The user's input.


    """
    # Print the prompt with a green background
    print(Fore.YELLOW + prompt + Style.RESET_ALL, end='')
    # Get user input
    user_input = input()
    return user_input


def print_input_instructions(instructions, color=Fore.WHITE):
    """
    Print input instructions with a specified color.

    Args:
        instructions (str): The instructions to be displayed.
        color (str, optional): The color of the instructions."
        " Defaults to Fore.MAGENTA.

    Returns:
        None
    """

    print()
    print(
        f"{Back.GREEN}{Fore.WHITE}{color}{' ' * 3} "
        f"{instructions.center(len(instructions) + 6)}"
        f"{' ' * 3}{Fore.RESET}{Back.RESET}"
    )


# DATA FUNCTIONS
def collect_player_info():
    """
    Collect player's name and location, and save it to Google Sheets.
    """
    print_input_instructions("Enter your name please")
    name = input_for_saving_info("Enter your name: ")

    print_input_instructions("Enter your location please")
    location = input_for_saving_info("Enter your location: ")

    # Append player information to the worksheet
    worksheet.append_row([name, location])

    print(f"Welcome to adventure {Fore.YELLOW}{name}{Fore.RESET} of "
          f"{Fore.YELLOW}{location}{Fore.RESET} let's save the Waldo.")


# PLAY GAME FUNCTIONS
collect_player_info()
