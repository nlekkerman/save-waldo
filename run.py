"""
Module: lock_cracker_game

This module contains functions related to the Lock Cracker game.
"""
import shutil
import random
import re
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

# players sheet
PLAYERS_WORKSHEET = 'players'
worksheet_players = SHEET.worksheet(PLAYERS_WORKSHEET)

# players sheet
RIDDLES_WORKSHEET = 'riddles'
worksheet_riddles = SHEET.worksheet(RIDDLES_WORKSHEET)


def upload_riddles_to_worksheet(worksheet):
    """
    Uploads a predefined list of riddles to a specified worksheet.

    Args:
        worksheet (Worksheet): The worksheet object where the riddles will be uploaded.

    Returns:
        None
    """
    # Define the list of riddles with their answers
    riddles = [
        ["What can you break without touching it?", "promise"],
        ["What has a heart that doesn't beat?", "n artichoke"],
        ["What has one eye but can't see?", "needle"],
        ["What has a face and two hands, but no arms or legs?", "clock"],
        ["What comes once in a minute, twice in a moment, but never in a thousand years?", "The letter 'M'"],
        ["What has many keys but can't open a single lock?", "typewriter"],
        ["I’m full of holes, yet I can hold water. What am I?", "net"],
        ["What has a bed but never sleeps, can run but never walks?", "river"],
        ["What can travel around the world while staying in a corner?", "stamp"],
        ["What has a neck but no head?", "bottle"],
        ["What has keys but can't open locks?", "piano"],
        ["What has hands but can't clap?", "clock"],
        ["What belongs to you but others use it more than you do?", "Your name"],
        ["What can be heard and caught but never seen?", "cold"],
        ["What is so fragile that saying its name breaks it?", "Silence"],
        ["What is full of holes but still holds water?", "sponge"]
    ]


    # Clear existing data in the worksheet
    worksheet.clear()

    # Define headers for the riddles
    headers = ["Riddle", "Answer"]

    # Append headers to the worksheet
    worksheet.append_row(headers)

    # Append each riddle and its answer to the worksheet
    for riddle, answer in riddles:
        worksheet.append_row([riddle, answer])


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


def input_for_password_level(prompt):
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
          " on the top of Paper Mountain." + Style.RESET_ALL)
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
    print_input_instructions("Enter your name please", Fore.WHITE)
    name = input_for_saving_info("Enter your name: ")

    print_input_instructions("Enter your location please", Fore.WHITE)
    location = input_for_saving_info("Enter your location: ")

    # Append player information to the worksheet
    worksheet_players.append_row([name, location])
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

"""
# PLAY GAME CALLS
greet_player_and_explain_game()
collect_player_info()
time.sleep(0.5)
print_centered_text("Challenge one, CRACK THE LOCK!!", Fore.RED)
time.sleep(0.5)
print_password_challenge_instructions()
"""

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


def reveal_password(password, guessed_numbers, revealed_positions):
    """
    Reveals the correct numbers guessed by the player.
    """
    revealed_numbers = [
        str(password[i]) if i in revealed_positions else '?' for i in range(4)
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

    print()
    print()
    print(Fore.RESET + Back.YELLOW + Fore.WHITE +
          "   ADVENTURER   " + Style.RESET_ALL)
    print()
    time.sleep(1)
    print(Back.WHITE + Fore.CYAN +
          " Now, I need you to stay focused! " + Style.RESET_ALL)
    print()
    time.sleep(1)
    print(Back.WHITE + Fore.CYAN +
          " You have to crack this lock to enter this castle! "
          + Style.RESET_ALL)
    print()
    time.sleep(1)
    print(Back.WHITE + Fore.CYAN +
          " Let's go and crack this 4-digit password! "
          + Style.RESET_ALL)
    print()
    time.sleep(1)
    print(Back.YELLOW + Fore.WHITE +
          " Hint: You have these two numbers in the password: "
          + Style.RESET_ALL +
          Fore.GREEN +
          f'({", ".join(map(str, hint_numbers))})' +
          Fore.RESET)

    # Initialize revealed positions to an empty list
    revealed_positions = []

    # Game loop
    while True:
        # Ask the player to guess the password
        print_input_instructions(
            "Enter your guess (4-digit number without spaces): ", Fore.YELLOW)
        guess = input_for_password_level("Enter 4-digits without spaces): ")

        # Check if the guess is correct
        if len(guess) != 4 or not guess.isdigit():
            print("Please enter a valid 4-digit number without spaces.")
            continue

        guess = [int(digit) for digit in guess]
        if guess == password:
            print(Fore.WHITE + Back.GREEN +
                  "Congratulations! You are in: " + Style.RESET_ALL + ' ',
                  Fore.YELLOW + Back.RED + "Password was " + ''.join(map(str, password))
                  + Style.RESET_ALL)
            break

        # Update revealed positions if any correct number is guessed
        for i in range(4):
            if guess[i] == password[i]:
                revealed_positions.append(i)

        revealed_password = reveal_password(
            password, hint_numbers, revealed_positions)
        print(Fore.RED + "Incorrect guess."
              " Here's the revealed part of the password:"
              + Fore.RESET + Fore.YELLOW, revealed_password
              + Style.RESET_ALL)
        print(Fore.RED + "Please try again." + Style.RESET_ALL)


#RIDDLE FUNCTIONS
def play_riddle_level():
    """
    Function to play the riddle level.
    """
    global SHEET

    print("\nYou have entered the castle and encountered the ghost of Enigma.")
    print("To proceed further, you must answer a riddle correctly.")
    print("You have 5 attempts to answer the riddle.")

    # Fetch riddles from the worksheet
    riddles_data = worksheet_riddles.get_all_values()[1:]  # Exclude header row

    # Set a random seed for reproducibility
    random.seed()
    random_riddle = random.choice(riddles_data)
    riddle, answer, hint_one, hint_two, hint_three = random_riddle

    attempts = 5
    hint_index = 0  # Initialize hint index
    while attempts > 0:
        print("\nRiddle:", riddle)
        try:
            user_answer = input("Your answer: ")
            # Validate user input
            if not re.match("^[a-zA-Z0-9\s]*$", user_answer):
                raise ValueError("Invalid input. Answer can only contain letters, spaces, and numbers.")
            # Check if user's answer is correct
            if user_answer.lower() == answer.lower():
                print("Congratulations! You have answered correctly.")
                break
            else:
                attempts -= 1
                if attempts > 0:
                    print("Incorrect answer. You have", attempts, "attempts remaining.")
                    # Display hint based on hint index
                    if hint_index == 0:
                        print("Hint One:", hint_one)
                    elif hint_index == 1:
                        print("Hint Two:", hint_two)
                    elif hint_index == 2:
                        print("Hint Three:", hint_three)
                    hint_index += 1  # Increment hint index for next attempt
                else:
                    print("Incorrect answer. You have run out of attempts. The ghost of Enigma has defeated you.")
        except ValueError as e:
            print(e)

# ROCK_PAPER_SCISSORS LEVEL
def play_rock_paper_scissors_level():
    """
    Function to play the rock-paper-scissors level against the enchanted knight, All Mighty Paper O'Clipper.
    """
    print("\nYou are one step away from entering the dark chamber where our friend Waldo is imprisoned.")
    print("In front of the doors stands an enchanted knight known as All Mighty Paper O'Clipper.")
    print("He challenges you to a duel with rock-paper-scissors to pass.")
    print("You have to beat him in a duel to 3 wins to proceed.")

    options = ['rock', 'paper', 'scissors']
    player_wins = 0
    computer_wins = 0

    while player_wins < 3 and computer_wins < 3:
        computer_choice = random.choice(options)

        player_choice = input("Enter your choice (r for rock, p for paper, s for scissors): ").lower()

        # Validate user input
        if player_choice not in ['r', 'p', 's']:
            print("Invalid input. Please enter 'r', 'p', or 's'.")
            continue

        # Convert player choice to full word
        if player_choice == 'r':
            player_choice = 'rock'
        elif player_choice == 'p':
            player_choice = 'paper'
        else:
            player_choice = 'scissors'

        print("All Mighty Paper O'Clipper's choice:", computer_choice)

        # Determine the winner
        if player_choice == computer_choice:
            print("It's a tie!")
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'paper' and computer_choice == 'rock') or \
             (player_choice == 'scissors' and computer_choice == 'paper'):
            print("Congratulations! You win this round!")
            player_wins += 1
        else:
            print("All Mighty Paper O'Clipper wins this round!")
            computer_wins += 1

        # Display the current score
        print("Your Score:", player_wins)
        print("All Mighty Paper O'Clipper's Score:", computer_wins)

    # Determine the overall winner
    if player_wins == 3:
        print("Congratulations! You have defeated All Mighty Paper O'Clipper and won the duel!")
    else:
        print("All Mighty Paper O'Clipper wins the duel. You have been defeated.")
        

# MAIN FUNCTION
def main():
    """
    Main function to orchestrate the game flow.
    """

    #play_password_level()
    #play_riddle_level()
    play_rock_paper_scissors_level()

if __name__ == "__main__":
    main()
