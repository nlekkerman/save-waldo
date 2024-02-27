"""
Module: lock_cracker_game

This module contains functions related to the Lock Cracker game.
"""
import shutil
import random
from random import shuffle, sample
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

# words sheet
WORDS_WORKSHEET = 'words'
worksheet_words = SHEET.worksheet(WORDS_WORKSHEET)


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
        f"{Back.BLUE}{Fore.WHITE}{color}{' ' * 3} "
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
        "To rescue him, you must crack the lock to enter the Castle,"
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


"""# PLAY GAME CALLS
greet_player_and_explain_game()
collect_player_info()
time.sleep(0.5)
print_centered_text("Challenge one, CRACK THE LOCK!!", Fore.RED)
time.sleep(0.5)
print_password_challenge_instructions()"""


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


def reveal_password(password, revealed_positions):
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
    time.sleep(0.5)
    print(Back.WHITE + Fore.CYAN +
          " Now, I need you to stay focused! " + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(Back.WHITE + Fore.CYAN +
          " You have to crack this lock to enter this castle! "
          + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(Back.WHITE + Fore.CYAN +
          " Let's go and crack this 4-digit password! "
          + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(Back.YELLOW + Fore.WHITE +
          " Hint: You have these two numbers in the password: "
          + Style.RESET_ALL +
          Fore.GREEN +
          f'({", ".join(map(str, hint_numbers))})' +
          Fore.RESET)

    # Initialize revealed positions to an empty list
    revealed_positions = []

    # Initialize attempts
    attempts = 10

    # Game loop
    while attempts > 0:
        # Ask the player to guess the password
        print_input_instructions(
            "Enter your guess (4-digit number without spaces). ")
        guess = input_for_password_level("Enter 4-digits without spaces: "
                                         + Fore.RESET)
        print(f"Attempts left: {Fore.BLUE}{attempts}\n", Fore.RESET)

        # Check if the guess is correct
        if len(guess) != 4 or not guess.isdigit():
            print(Fore.RED +
                  "Please enter a valid 4-digit number without spaces."
                  + Fore.RESET)
            continue
        print(Back.YELLOW + Fore.WHITE +
              " Hint: You have these two numbers in the password: "
              + Style.RESET_ALL +
              Fore.GREEN +
              f'({", ".join(map(str, hint_numbers))})' +
              Fore.RESET)
        guess = [int(digit) for digit in guess]
        attempts -= 1
        if guess == password:
            print()
            print(Fore.WHITE + Back.GREEN +
                  "Congratulations! You are in: " + Style.RESET_ALL + ' ',
                  Fore.YELLOW + Back.RED + "Password was "
                  + ''.join(map(str, password))
                  + Style.RESET_ALL)
            return True

        # Update revealed positions if any correct number is guessed
        for i in range(4):
            if guess[i] == password[i]:
                revealed_positions.append(i)

        revealed_password = reveal_password(
            password, revealed_positions)
        print(Fore.RED + "Incorrect guess! The password:"
              + Fore.RESET + Fore.YELLOW, revealed_password
              + Style.RESET_ALL)
        print(Fore.RED + f"Attempts left: {attempts}. Please try again."
              + Style.RESET_ALL)

    print(Fore.RED +
          "Sorry, you've run out of attempts. Better luck next time!"
          + Fore.RESET)
    return False


# RIDDLE FUNCTIONS
def play_riddle_level():
    """
    Function to play the riddle level.
    """

    print()
    print(Back.WHITE + Fore.GREEN +
          "You've completed the first step to save Waldo!"
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN +
          "You've cracked the lock and you have entered the castle and encountered the ghost called Enigma."
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN +
          "Now Enigma, once a powerful wizard,"
          " a slave of the Queen of Bureaucracy,"
          " stares at you with hollow eyes."
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN +
          "He has a deadly challenge for you." + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN +
          "He has a riddle for you. If you answer correctly, you can proceed,"
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN
          + "but if you answer wrongly, he will enchant you. "
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN +
          "And you will spend the rest of your life"
          " as a printer machine in the Queen's office."
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN + "You have 5 attempts to answer the riddle." 
          + Style.RESET_ALL)
    time.sleep(0.5)
    print()
    print(Back.WHITE + Fore.GREEN +
          "You have 5 attempts to answer the riddle." + Style.RESET_ALL)
    print()

    # Fetch riddles from the worksheet
    riddles_data = worksheet_riddles.get_all_values()[1:]

    # Set a random seed for reproducibility
    random.seed()
    random_riddle = random.choice(riddles_data)
    riddle, answer, hint_one, hint_two, hint_three = random_riddle

    attempts = 5
    hint_index = 0  # Initialize hint index
    while attempts > 0:
        print(Back.YELLOW + Fore.WHITE + " THE RIDDLE:   "
              + Style.RESET_ALL)
        print(Back.BLUE + Fore.WHITE + riddle + Style.RESET_ALL)
        user_answer = input_for_saving_info("Enter the Riddle: ")
        # Validate user input
        if not re.match(r"^[a-zA-Z\s]*$", user_answer):
            print(Fore.RED + "Invalid input. Answer can only contain letters,"
                  " spaces, and numbers." + Fore.RESET)
            continue

        if user_answer.lower() == answer.lower():
            print(Fore.GREEN + "Congratulations! You have answered correctly." 
                  + Fore.RESET)
            return True
        attempts -= 1
        if attempts > 0:
            print(Fore.RED + 
                  "Incorrect!. You have", attempts, "attempts remaining." 
                  + Fore.RESET)
            # Display hint based on hint index
            if hint_index == 0:
                print(Fore.GREEN + "Hint One:", hint_one + Fore.RESET)
            elif hint_index == 1:
                print(Fore.GREEN + "Hint Two:", hint_two + Fore.RESET)
            elif hint_index == 2:
                print(Fore.GREEN + "Hint Three:", hint_three + Fore.RESET)
            hint_index += 1  # Increment hint index for next attempt
        else:
            print(Fore.RED + "Incorrect answer. You have run out of attempts."
                  " The ghost of Enigma has defeated you." + Fore.RESET)
            print()
            print(Back.WHITE + Fore.RED + "RIDDLE WAS:" + Fore.RESET + " "
                  + Fore.YELLOW + riddle + Style.RESET_ALL)
            print()
            
            return False

    return False  # loop ends without the player answering correctly


def play_rock_paper_scissors_level():
    """
    Function to play the rock-paper-scissors level "
    "against the enchanted knight, All Mighty Paper O'Clipper.
    """
    print("\nYou are one step away from entering the dark chamber"
          " where our friend Waldo is imprisoned.")
    print("In front of the doors stands an enchanted knight known"
          " as All Mighty Paper O'Clipper.")
    print("He challenges you to a duel with rock-paper-scissors to pass.")
    print("You have to beat him in a duel to 3 wins to proceed.")

    options = ['rock', 'paper', 'scissors']
    player_wins = 0
    computer_wins = 0

    while player_wins < 3 and computer_wins < 3:
        computer_choice = random.choice(options)
        print(computer_choice)

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
        elif player_choice == 'rock' and computer_choice == 'scissors':
            print("Congratulations! You win this round!")
            player_wins += 1
        elif player_choice == 'paper' and computer_choice == 'rock':
            print("Congratulations! You win this round!")
            player_wins += 1
        elif player_choice == 'scissors' and computer_choice == 'paper':
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
        return True
    else:
        print("All Mighty Paper O'Clipper wins the duel. You have been defeated.")
        return False


# THE WORD MAZE GAME
def generate_maze_sequence(length):
    """
    Generate a random sequence of left (L) and right (R) directions for the maze.
    """
    directions = ['L', 'R']  # Left and right directions
    maze_sequence = [random.choice(directions) for _ in range(length)]
    return maze_sequence


def print_warning():
    """
    Prints a warning message every 10 seconds.
    """
    while True:
        print("Warning: Time is passing!")
        time.sleep(10)  # Sleep for 10 seconds before printing the next warning


def play_word_maze_level():
    """
    Function to play the word maze game.
    """
    maze_sequence = generate_maze_sequence(5)
    max_wrong_attempts = 3
    correct_answers = 0
    wrong_attempts = 0
    print(maze_sequence)

    print(
        Back.WHITE + Fore.RED +
        "\nWelcome to the Word Maze Game!"
        + Style.RESET_ALL)
    print("Waldo's cage is at the end of the maze.")
    print("The maze is collapsing, and you need to guess"
          " the correct sequence of left (L) and right (R) turns.")
    print("Be careful! Making too many wrong guesses"
          " might lead to unexpected dangers!")

    # Gameplay loop
    index = 0
    while index < len(maze_sequence):
        direction = maze_sequence[index]
        print(f"Guess the direction ({index + 1}/5): ")
        player_guess = input().upper()

        # Validate player's input
        if player_guess not in ['L', 'R']:
            print(Fore.RED +
                  "Invalid input. Please enter 'L' for left or 'R' for right."
                  + Style.RESET_ALL)
            continue

        # Check if player's guess matches the maze sequence
        if player_guess == direction:
            print("Correct guess!")
            correct_answers += 1
            index += 1
        else:
            print(
                Fore.MAGENTA +
                "Incorrect guess. The maze seems to shift unexpectedly!"
                + Style.RESET_ALL)
            print(f"Oh no, that was a dead end! You have "
                  f"{max_wrong_attempts - wrong_attempts - 1} "
                  "attempts remaining.")
            wrong_attempts += 1

            # Check if maximum wrong attempts reached
            if wrong_attempts >= max_wrong_attempts:
                print("The maze has collapsed completely!")
                return False

    print("Congratulations! You've reached Waldo's cage!")
    return True


# MAGIC WORDS FUNCTIONS/S
def get_random_word():
    """
    Function to retrieve a random word from the Google Sheet.
    """
    # Get all words from the sheet
    words_data = worksheet_words.get_all_values()[1:]  # Exclude header row

    # Shuffle the words
    shuffle(words_data)

    # Select a random word
    random_word = sample(words_data, 1)[0]

    # Extract the unscrambled word
    unscrambled_word = random_word[0]

    # Extract the scrambled word
    scrambled_word = random_word[1]
    print(scrambled_word + "  " + unscrambled_word)
    return unscrambled_word, scrambled_word


def play_say_magic_word_level():
    """
    Function to play the word guessing game.
    """

    unscrambled_word, scrambled_word = get_random_word()
    print("\nCongratulations, adventurer! You stand before Waldo's cage.")
    print("To unlock the cage and free Waldo,"
          "you must speak the magic word within 1 minute.")
    print("Be warned, you have only 1 minute to guess the word!")
    print("Every guess, a warning will be issued.")
    print(f"\nScrambled word: {scrambled_word}")

    start_time = time.time()
    end_time = start_time + 60  # 1 minute

    while True:
        current_time = time.time()
        remaining_time = end_time - current_time

        if remaining_time >= 0:
            print(f"\nRemaining time: {int(remaining_time)} seconds.")

        if current_time >= end_time:
            print("\nTime's up! "
                  "The cage remains locked. "
                  "Waldo remains trapped.")

            return False

        player_guess = input(
            "Enter the unscrambled magic word: ").strip().lower()
        if player_guess == unscrambled_word:
            print("\nCongratulations! You've spoken the magic word!")
            print("Waldo's cage is now unlocked. You have freed him!")
            return True


# PLAY GAME FUNCTIION
def play_game():
    """
    Plays a multi-level game consisting of various challenges.

    Returns:
        None
    """

    if not play_password_level():
        print("Sorry, you failed to complete the game. Better luck next time!")
        return

    if not play_riddle_level():
        print("Sorry, you failed to complete the game. Better luck next time!")
        return

    if not play_rock_paper_scissors_level():
        print("Sorry, you failed to complete the game. Better luck next time!")
        return

    if not play_word_maze_level():
        print("Sorry, you failed to complete the game. Better luck next time!")
        return

    if not play_say_magic_word_level():
        print("Sorry, you failed to complete the game. Better luck next time!")
        return

    print("Congratulations! You've completed all levels of the game!")


# MAIN FUNCTION
def main():
    """
    Main function to orchestrate the game flow.
    """
    play_game()


if __name__ == "__main__":
    main()
