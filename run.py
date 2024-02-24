"""
Module: lock_cracker_game

This module contains functions related to the Lock Cracker game.
"""
import shutil
import random
import time
from colorama import init, Fore, Back, Style
import gspread
from google.oauth2.service_account import Credentials

TERMINAL_WIDTH = shutil.get_terminal_size().columns

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


# Inputs related function
def input_for_saving_info(prompt):
    """
    Prompt the user for input with explanatory text and a green background.

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


# DATA  AND INFO FUNCTIONS
def greet_player_and_explain_game():
    """
    Greets the player and explains the game with colors and delays.
    """
    print(Fore.GREEN + Back.WHITE + "WELCOME ADVENTURER!" + Style.RESET_ALL)
    time.sleep(1)
    print(
        Fore.MAGENTA +
        "Before we proceed, let me provide some context:" + Style.RESET_ALL)
    print(
        Fore.MAGENTA + "You remeber your friend Waldo, right?"
        + Style.RESET_ALL)
    time.sleep(1)
    print(Fore.MAGENTA +
          "Nobody knows where Waldo was,"
          "because he was ensnared by the crazy Queen Vladislava."
          + Style.RESET_ALL)
    time.sleep(1)
    print(Fore.MAGENTA + "She ruled the Bureaucracy Kingdom from her castle"
          " on the top of Paper Mountain." + Style.RESET_ALL)3121
    time.sleep(1)
    print(Fore.MAGENTA +
          "In this quest, we will go through challenges to save Waldo,"
          + Style.RESET_ALL)
    time.sleep(1)
    print(Fore.MAGENTA + "You are Waldo's last hope!" + Style.RESET_ALL)
    time.sleep(1)
    print(Fore.MAGENTA + "Are you ready to embark on this adventure?"
          + Style.RESET_ALL)

    print()


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
    print()
    print(f"Welcome to adventure {Fore.YELLOW}{name}{Fore.RESET} of "
          f"{Fore.YELLOW}{location}{Fore.RESET} let's save the Waldo.")


def print_password_challenge_instructions():
    """
    Print the first game instructions.

    Returns:
        None
    """
    instructions = [
        "You find yourself standing in front of the imposing Dark Castle,"
        " shrouded in darkness and mystery.",
        "Buddy Waldo, your dear friend, is imprisoned"
        " within these walls, alone and scared.",
        "You are his only hope for freedom and salvation.",
        "To rescue him, you must crack the lock protecting his cell,"
        " a formidable 4-digit password lock.",
        "The password consists of numbers ranging from 0 to 5,"
        " each digit adding to the challenge.",
        "Enter a 4-digit number without spaces to make your guess"
        " and unlock Waldo's prison.",
        "Good luck on your daring mission!"
    ]
    color = Fore.GREEN  # Set green color for the text

    for rule in instructions:
        padding_rule = (TERMINAL_WIDTH - len(rule)) // 2
        centered_rule = f"{'' * padding_rule}{rule}{' ' * padding_rule}"
        print(f"{color}{Style.BRIGHT}{centered_rule}{Style.RESET_ALL}")


def print_centered_text(text, color):
    """
    Print centered text with specified color.

    Args:
        text (str): The text to be centered and printed.
        color (str): The color of the text.

    Returns:
        None
    """
    padding_for_centered = (TERMINAL_WIDTH - len(text)) // 2

    print(
        f"{Back.WHITE}{color}"
        f"{' ' * padding_for_centered}"
        f"{text}"
        f"{' ' * padding_for_centered}"
        f"{Style.RESET_ALL}"
    )
    print()


# PLAY GAME CALLS
greet_player_and_explain_game()
collect_player_info()
time.sleep(0.5)
print_centered_text("Challenge one, CRACK THE LOCK!!", Fore.RED)
time.sleep(0.5)
print_password_challenge_instructions()


# PASSWORD LEVEL FUNCTIONS
def generate_password():
    """
    Generates a 4-digit password.
    """
    return [random.randint(0, 5) for _ in range(4)]


def provide_hint(password):
    """
    Provides a hint to the player by revealing two numbers in the password.
    """
    hint_numbers = random.sample(password, 2)
    return hint_numbers


def reveal_password(password, guessed_numbers):
    """
    Reveals the correct numbers guessed by the player.
    """
    revealed_numbers = [
        '?' if i not in guessed_numbers else str(password[i])
        for i in range(4)
    ]
    return ' '.join(revealed_numbers)


def play_password_level():
    """
    Orchestrates the password guessing game.
    """
    # Generate the password
    password = generate_password()
    print(password)
    # Provide hint to the player
    hint_numbers = provide_hint(password)

    print("Welcome to the Password Guessing Game!")
    print("Try to guess the 4-digit password.")
    print("Hint: You have these two numbers in the password:", hint_numbers)

    # Game loop
    while True:
        # Ask the player to guess the password
        guess = input("Enter your guess (4-digit number without spaces): ")

        # Check if the guess is correct
        if len(guess) != 4 or not guess.isdigit():
            print("Please enter a valid 4-digit number without spaces.")
            continue

        guess = [int(digit) for digit in guess]
        if guess == password:
            print("Congratulations! You've guessed the correct password:", ''.join(map(str, password)))
            break
        else:
            revealed_password = reveal_password(password, hint_numbers)
            print("Incorrect guess. Here's the revealed part of the password:", revealed_password)
            print("Please try again.")


# MAIN FUNCTION
def main():
    """
    Main function to orchestrate the game flow.
    """

    play_password_level()


if __name__ == "__main__":
    main()
