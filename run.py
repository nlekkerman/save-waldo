"""
Module: lock_cracker_game

This module contains functions
related to the Lock Cracker game.
"""
import shutil
import os
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
PLAYERS_WORKSHEET = 'players'
worksheet_players = SHEET.worksheet(PLAYERS_WORKSHEET)
RIDDLES_WORKSHEET = 'riddles'
worksheet_riddles = SHEET.worksheet(RIDDLES_WORKSHEET)
WORDS_WORKSHEET = 'words'
worksheet_words = SHEET.worksheet(WORDS_WORKSHEET)
SCORES_WORKSHEET = 'scores'
worksheet_scores = SHEET.worksheet(SCORES_WORKSHEET)


# Inputs related function
def input_for_saving_info(prompt):
    """
    Prompt the user for input with explanatory text and a green background.
    Parameters:
    - prompt (str): The prompt message to display to the user.
    Returns:
    - str: The user's input.
    """
    print(Fore.YELLOW + prompt + Style.RESET_ALL, end='')
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
    print(Fore.YELLOW + prompt + Style.RESET_ALL, end='')
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


def print_validation_error(error_message):
    """
    Prints a validation error message in red text.
    """
    print(Fore.RED + error_message + Style.RESET_ALL)


def print_positive_messages(positive_message):
    """
    Prints a validation error message in red text.
    """
    print(Fore.GREEN + positive_message + Style.RESET_ALL)


def print_level_passed_message(message):
    """
    Prints a message with green background and white letters.
    """
    print(Back.GREEN + Fore.WHITE + message + Style.RESET_ALL)


def print_congratulations_message(message):
    """
    Function to print a personalized congratulatory message
    centered on the screen with colorama.
    """
    print("\n" * 3)
    print_empty_line_with_color()
    print_centered_text(message, Fore.GREEN)
    print_empty_line_with_color()


def print_empty_line_with_color():
    """
    Prints an empty line with each character"
    " having a different background color.
    Returns:
        None
    """
    line_length = TERMINAL_WIDTH
    # Choose a random color for each character and print the line
    color_line = ""
    for _ in range(line_length):
        color_code = random.randint(40, 47)
        color_line += f"\033[{color_code}m \033[0m"
    print(color_line)


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


def print_separation_lines(color):
    """
    Print centered text with specified color.
    Args:
        text (str): The text to be centered and printed.
        color (str): The color of the text.
    Returns:
        None
    """
    lines = "======================================================"
    padding_for_centered = (TERMINAL_WIDTH - len(lines)) // 2
    print(
        f"{Back.WHITE}{color}"
        f"{' ' * padding_for_centered}"
        f"{lines}"
        f"{' ' * padding_for_centered}"
        f"{Style.RESET_ALL}"
    )


def clear_screen():
    """
    Function to clear the terminal screen.
    """
    os.system('cls' if os.name == 'nt' else 'clear')


# DATA  AND INFO FUNCTIONS
def greet_player_and_explain_game():
    """
    Greets the player and explains the game with colors and delays.
    """
    print()
    time.sleep(0.5)
    print(
        Fore.GREEN +
        "In the realm of mysteries and shadows, a tale unfolds."
        + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(
        Fore.GREEN +
        "A dear friend, Waldo, lies ensnared in the clutches"
        " of the enigmatic Queen Vladislava."
        + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(
        Fore.GREEN +
        "Her dominion, the Bureaucracy Kingdom, casts a looming shadow"
        " from her castle atop the towering Paper Mountain."
        + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(
        Fore.GREEN +
        "In this odyssey, we beckon you forth, the beacon of hope"
        " in Waldo's darkest hour."
        + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(
        Fore.GREEN +
        "For you are the last hope, the valiant soul,"
        " destined to rescue him."
        + Style.RESET_ALL)
    print()
    time.sleep(0.5)
    print(
        Fore.GREEN +
        "Are you prepared to embark on this perilous journey?"
        + Style.RESET_ALL)

    print()


def is_valid_input(name):
    """
    Function to validate the player's name.

    Args:
        name (str): The player's name to validate.

    Returns:
        bool: True if the name is valid, False otherwise.
    """
    if not name:
        return False

    has_alpha = False
    previous_char = ''
    for char in name:
        if char.isalpha():
            has_alpha = True
            previous_char = char
        elif char == ' ':
            if previous_char == ' ':
                return False
            if not has_alpha:
                return False
            previous_char = char
        elif char == "'":
            if previous_char == ' ':
                return False
            previous_char = char
        else:
            return False
    return has_alpha


def collect_player_info():
    """
    Collect player's name and location, and save it to Google Sheets.

    Returns:
        name (str): The player's name.
        location (str): The player's location.
    """
    name = None
    location = None

    while not name or not location:
        if not name:
            print_input_instructions("Enter your name please", Fore.WHITE)
            name = input_for_saving_info("Enter your name: ")

            if not is_valid_input(name):
                print_validation_error(
                    "Invalid input. Please enter only letters and apostrophes."
                    )
                name = None
            continue

        if not location:
            print_input_instructions("Enter your location please", Fore.WHITE)
            location = input_for_saving_info("Enter your location: ")

            if not is_valid_input(location):
                print_validation_error(
                    "Invalid input. Please enter only letters and spaces.")
                location = None
            continue

    worksheet_players.append_row([name, location])
    print()
    print()
    print_empty_line_with_color()
    print_centered_text(" Welcome to adventure ", Fore.GREEN)
    print_centered_text(name, Fore.RED)
    print_centered_text(" of ", Fore.GREEN)
    print_centered_text(location, Fore.RED)
    print_empty_line_with_color()
    print()
    print()
    time.sleep(4)
    return name, location


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
        "To rescue him,first you must crack the lock to enter the Castle,"
        " a formidable 4-digit password lock.",
        "The password consists of numbers ranging from 0 to 5,"
        " each digit adding to the challenge.",
        "Enter a 4-digit number without spaces to make your guess"
        " and unlock Waldo's prison.",
        "Good luck on your daring mission!"

    ]
    color = Fore.GREEN
    for rule in instructions:
        padding_rule = (TERMINAL_WIDTH - len(rule)) // 2
        centered_rule = f"{'' * padding_rule}{rule}{' ' * padding_rule}"
        print(f"{color}{Style.BRIGHT}{centered_rule}{Style.RESET_ALL}")
        print()
        time.sleep(0.5)


def record_score(name, location, time_taken):
    """
    Record the player's score (name, location, time taken)
    in the scores worksheet.
    """
    # Round time_taken to seconds
    time_taken_rounded = round(time_taken)
    worksheet_scores.append_row([name, location, time_taken_rounded])


def print_leaderboard(worksheet):
    """
    Print the leaderboard based on the best times of players.

    Args:
        worksheet (gspread.Worksheet):
        The worksheet containing the leaderboard data.

    Returns:
        None
    """
    print_colored_text("Leaderboard (Sorted by Best Time):")
    print()
    words = ["Name      ", "Country      ", "Time   "]
    colors = [Back.RED, Back.GREEN, Back.MAGENTA]
    print_board_categories(words, colors)
    print(Style.RESET_ALL)
    leaderboard_data = worksheet.get_all_values()[1:]
    leaderboard_data.sort(
        key=lambda x: float(x[-1]) if x[-1] else float('inf')
        )

    for i, row in enumerate(leaderboard_data[:10]):
        if i == 0:
            medal_color = Fore.YELLOW
        elif i == 1:
            medal_color = Fore.CYAN
        elif i == 2:
            medal_color = Fore.RED
        else:
            medal_color = Fore.RESET

        print(
            f"{medal_color}{row[0]:<10} {row[1]:<14} {row[2]}"
        )


def print_colored_text(text, background_color=None):
    """
    Print the text "Congratulations!" with each letter in a different color.

    Args:
        text (str): The text to print.

    Returns:
        None
    """
    colored_letters = [
        Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN]
    centered_text = text.center(TERMINAL_WIDTH)
    colored_text = ""
    for insx, char in enumerate(centered_text):
        colored_text += (
                         f"{colored_letters[insx % len(colored_letters)]}"
                         f"{Style.BRIGHT}{char}"
                        )
    # Apply background color if provided
    if background_color:
        print(f"{background_color}{colored_text}{Style.RESET_ALL}")
    else:
        print(colored_text)


def print_board_categories(words_text, words_colors):
    """
    Print each word in a different color.

    Args:
        words (list): List of words to print.
        colors (list): List of colorama color codes corresponding to each word.

    Raises:
        ValueError: If the length of the words and colors lists don't match.
    """
    if len(words_text) != len(words_colors):
        raise ValueError("The lengths of words and colors lists must match.")

    # Construct the text with specified colors for each word
    colored_text = ""
    for word, color in zip(words_text, words_colors):
        colored_text += f"{color}{word} "

    # Print the colored text
    print(colored_text.strip() + Style.RESET_ALL)


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
    clear_screen()
    print_separation_lines(Fore.RED)
    print_centered_text("Welcome to Challenge One: CRACK THE LOCK!!", Fore.RED)
    print_separation_lines(Fore.RED)
    # Generate the password
    password = generate_password()
    print(password)
    # Provide hint to the player
    hint_numbers = provide_hint(password)

    print_password_challenge_instructions()
    time.sleep(0.5)
    print(Back.YELLOW + Fore.WHITE +
          "Hint: You have these two numbers in the password: "
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
        print(f"{Fore.BLUE}Attempts left:{Fore.RESET}{Fore.YELLOW}"
              f" {attempts}\n", Fore.RESET + Back.RESET)

        # Check if the guess is correct
        if len(guess) != 4 or not guess.isdigit():
            print(Fore.RED +
                  "Please enter a valid 4-digit number without spaces."
                  + Fore.RESET)
            continue
        print(Fore.BLUE +
              "Hint: You have these two numbers in the password: "
              + Style.RESET_ALL +
              Fore.YELLOW + " " +
              f'({", ".join(map(str, hint_numbers))})' +
              Fore.RESET)
        guess = [int(digit) for digit in guess]
        attempts -= 1
        if guess == password:
            print()
            print_congratulations_message(
                "Congratulations! You've unlocked the doors"
                " to the castle atop the paper mountain.")
            print()
            return True

        # Update revealed positions if any correct number is guessed
        for i in range(4):
            if guess[i] == password[i]:
                revealed_positions.append(i)

        # Check if all numbers are revealed
        if len(revealed_positions) == 4:
            print(Fore.GREEN +
                  "All numbers are revealed!"
                  " Please enter the complete password now: "
                  + Fore.RESET + Fore.YELLOW + ''.join(map(str, password))
                  + Fore.RESET)
            continue

        revealed_password = reveal_password(
            password, revealed_positions)
        print(Fore.RED + "Incorrect guess! The password:"
              + Fore.RESET + Fore.YELLOW, revealed_password
              + Style.RESET_ALL)
        print()
        print(f"{Fore.BLUE}Attempts left:{Fore.RESET}{Fore.YELLOW}"
              f"{attempts}\n", Fore.RESET + Back.RESET)

    print(Fore.RED +
          "Sorry, you've run out of attempts. Better luck next time!"
          + Fore.RESET)
    return False


# RIDDLE FUNCTIONS
def print_instruction_message(message, color=Fore.GREEN
                              ):
    """Prints a message with specified color and background."""
    print(Fore.RESET)
    print(color + message + Style.RESET_ALL)
    time.sleep(0.5)


def get_random_riddle(riddles_data):
    """Selects a random riddle from a list of riddles."""
    random.seed()
    return random.choice(riddles_data)


def print_hint(hint):
    """Prints a hint."""
    print(Fore.BLUE + hint + Fore.RESET)


def validate_answer(answer):
    """Validates user's answer."""
    return re.match(r"^[a-zA-Z\s]*$", answer)


def play_riddle(riddle, answer, hints):
    """Plays the riddle game."""
    attempts = 5
    hint_index = 0
    while attempts > 0:
        print()
        print(Fore.WHITE + Back.YELLOW + " THE RIDDLE:  " + Style.RESET_ALL)
        print(Fore.WHITE + Back.BLUE + riddle + Fore.RESET + Back.RESET)
        user_answer = input_for_saving_info("Enter the answer: ")
        if not validate_answer(user_answer):
            print_validation_error(
                "Invalid input. Answer can only contain letters,"
                " spaces, and numbers.")
            continue
        if user_answer.lower() == answer.lower():
            print_congratulations_message(
                "Congratulations! Your wit shines bright"
                " as you solve the riddle correctly.")
            print()
            return True
        attempts -= 1
        if attempts > 0:
            print(
                Fore.RED +
                f"Incorrect! You have {Fore.RESET}{Fore.YELLOW}{attempts} "
                f"{Fore.RESET}{Fore.RED} attempts remaining."
                + Fore.RESET)
            if hint_index < len(hints):
                print_hint(f"{Fore.BLUE}Hint{Fore.RESET} "
                           f"{hint_index + 1}:{Fore.YELLOW}"
                           f" {hints[hint_index]}"
                           + Style.RESET_ALL)
                hint_index += 1
        else:
            print_instruction_message(
                "Incorrect answer. You have run out of attempts."
                " The ghost of Enigma has defeated you.", Fore.RED)
            print(
                Fore.BLUE + "RIDDLE WAS: " + Fore.RESET + Fore.YELLOW
                + answer + Fore.RESET)
            print()
            print()
            return False

    return False


def play_riddle_level():
    """Plays the riddle level."""
    time.sleep(4)
    clear_screen()
    print_separation_lines(Fore.RED)
    print_centered_text(
        "Welcome to Challenge Two: ANSWER THE RIDDLE!!", Fore.RED)
    print_separation_lines(Fore.RED)
    print_instruction_message("You've completed the first step to save Waldo!")
    print_instruction_message("You've cracked the lock and you have"
                              " entered the castle and encountered"
                              " the ghost called Enigma.")
    print_instruction_message("Now Enigma, once a powerful wizard,"
                              " a slave of the Queen of Bureaucracy,"
                              " stares at you with hollow eyes.")
    print_instruction_message("He has a deadly challenge for you.")
    print_instruction_message("He presents you with a riddle, "
                              "his eyes glinting with challenge,"
                              " as if daring you to solve it. ")
    print_instruction_message("If you answer correctly, you can proceed,"
                              " but if you answer wrongly,"
                              " he will enchant you.")
    print_instruction_message("And you will spend the rest of your life"
                              " as a printer machine in the Queen's office.")
    print_instruction_message("You have 5 attempts to answer the riddle.")
    # Fetch riddles from the worksheet
    riddles_data = worksheet_riddles.get_all_values()[1:]
    random_riddle = get_random_riddle(riddles_data)
    riddle, answer, *hints = random_riddle
    return play_riddle(riddle, answer, hints)


def play_rock_paper_scissors_level():
    """
    Function to play the rock-paper-scissors level "
    "against the enchanted knight, All Mighty Paper O'Clipper.
    """
    time.sleep(2)
    clear_screen()
    print_separation_lines(Fore.RED)
    print_centered_text("Welcome to Challenge Three:"
                        " ROCK,PAPER or SISSORS DUEL!!", Fore.RED)
    print_separation_lines(Fore.RED)
    print_instruction_message("You are three step away from"
                              " entering the dark chamber"
                              " where our friend Waldo is imprisoned.")
    print_instruction_message("In front of the doors stands"
                              " an enchanted knight known"
                              " as All Mighty Paper O'Clipper.")
    print_instruction_message("He challenges you to a duel"
                              " with rock-paper-scissors to pass.")
    print_instruction_message("You have to beat him"
                              " in a duel to 3 wins to proceed.")
    options = ['rock', 'paper', 'scissors']
    player_wins = 0
    computer_wins = 0
    while player_wins < 3 and computer_wins < 3:
        computer_choice = random.choice(options)
        print(computer_choice)
        print_input_instructions(
            "Enter your choice (r for rock, p for paper, s for scissors): "
            )
        player_choice = input_for_saving_info("Your choice ").lower()
        # Validate user input
        if player_choice not in ['r', 'p', 's']:
            print_validation_error(
                "Invalid input. Please enter 'r', 'p', or 's'."
                )
            continue
        # Convert player choice to full word
        if player_choice == 'r':
            player_choice = 'rock'
        elif player_choice == 'p':
            player_choice = 'paper'
        else:
            player_choice = 'scissors'

        print(Fore.CYAN + "All Mighty Paper O'Clipper's choice: ", Fore.RESET
              + Fore.YELLOW + computer_choice + Fore.RESET)

        # Determine the winner
        if player_choice == computer_choice:
            print(Back.WHITE + Fore.BLUE + "It's a tie!" + Style.RESET_ALL)
        elif player_choice == 'rock' and computer_choice == 'scissors':
            print_positive_messages("Congratulations! You win this round!")
            player_wins += 1
        elif player_choice == 'paper' and computer_choice == 'rock':
            print_positive_messages("Congratulations! You win this round!")
            player_wins += 1
        elif player_choice == 'scissors' and computer_choice == 'paper':
            print_positive_messages("Congratulations! You win this round!")
            player_wins += 1
        else:
            print("All Mighty Paper O'Clipper wins this round!")
            computer_wins += 1
        # Display the current score
        print(Fore.YELLOW + "Your Score: "
              + Fore.RESET, Fore.RED + str(player_wins) + Fore.RESET)

        print(Fore.YELLOW + "All Mighty Paper O'Clipper's Score:"
              + Fore.RESET, Fore.RED + str(computer_wins) + Fore.RESET)
    # Determine the overall winner
    if player_wins == 3:
        print()
        print_empty_line_with_color()
        print_centered_text("Congratulations! You have defeated"
                            " All Mighty Paper O'Clipper"
                            " and won the duel!", Fore.GREEN)
        print_empty_line_with_color()
        print()
        return True
    print("All Mighty Paper O'Clipper wins the duel. You have been defeated.")
    return False


# THE WORD MAZE GAME
def generate_maze_sequence(length):
    """
    Generate a random sequence of left (L)
    and right (R) directions for the maze.
    """
    directions = ['L', 'R']  # Left and right directions
    maze_sequence = [random.choice(directions) for _ in range(length)]
    return maze_sequence


def play_word_maze_level():
    """
    Function to play the word maze game.
    """
    time.sleep(4)
    clear_screen()
    print_separation_lines(Fore.RED)
    print_centered_text("Welcome to Challenge Four: PASS THE MAZE!!", Fore.RED)
    print_separation_lines(Fore.RED)
    maze_sequence = generate_maze_sequence(5)
    max_wrong_attempts = 3
    correct_answers = 0
    wrong_attempts = 0
    print(maze_sequence)
    print_instruction_message(
        "Before you, our valiant adventurer, passed O'clipper,")
    print_instruction_message(
        "the knight, in an exhausting duel,"
        " where the clash of words sang the ballad of bravery and resilience.")
    print_instruction_message(
        "Behold, the new leg of your journey awaits - Waldo's"
        " cage lies at the end of the labyrinth, hidden")
    print_instruction_message(
        "amidst the shadows and whispers of the ancient stones.")
    print_instruction_message(
        "The maze, now stirred by your presence,"
        " begins to tremble and collapse,")
    print_instruction_message(
        "its winding paths shifting like the sands of time."
        " Only by discerning the correct sequence of left (L) and right (R)"
        "turns can you navigate its treacherous embrace.")
    print_instruction_message(
        "But heed this warning, noble soul: with each misstep,"
        " the specter of unforeseen perils looms closer,")
    print_instruction_message(
        "waiting to ensnare the unwary wanderer. Tread carefully,"
        " for the labyrinth guards its secrets jealously.")
    index = 0
    while index < len(maze_sequence):
        direction = maze_sequence[index]
        print_input_instructions(
            f"Guess the direction, L for left od R for right ({index + 1}/5): "
            )
        player_guess = input_for_saving_info("Choose direction ").upper()
        # Validate player's input
        if player_guess not in ['L', 'R']:
            print_validation_error(
                "Invalid input. Please enter 'L' for left or 'R' for right.")
            continue
        # Check if player's guess matches the maze sequence
        if player_guess == direction:
            print_positive_messages("Correct guess!")
            correct_answers += 1
            index += 1
        else:
            print_validation_error("Incorrect guess."
                                   " The maze seems to shift unexpectedly!")
            print_validation_error(f"Oh no, that was a dead end! You have "
                                   f"{max_wrong_attempts - wrong_attempts - 1}"
                                   f" attempts remaining.")
            wrong_attempts += 1
            # Check if maximum wrong attempts reached
            if wrong_attempts >= max_wrong_attempts:
                print(Back.WHITE + Fore.RED +
                      "The maze has collapsed completely!" + Style.RESET_ALL)
                return False
    print()
    print_empty_line_with_color()
    print_centered_text(
        "Congratulations! You've reached Waldo's cage!", Fore.GREEN)
    print_empty_line_with_color()
    print()
    return True


# MAGIC WORDS FUNCTIONS/S
def get_random_word():
    """
    Function to retrieve a random word from the Google Sheet.
    """
    # Get all words from the sheet
    words_data = worksheet_words.get_all_values()[1:]
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


def play_magic_word_level():
    """
    Function to play the word guessing game.
    """
    time.sleep(4)
    clear_screen()
    print_separation_lines(Fore.RED)
    print_centered_text(
        "Welcome to the Final Challenge : SAY MAGIC WORD!!", Fore.RED)
    print_separation_lines(Fore.RED)
    unscrambled_word, scrambled_word = get_random_word()
    print()
    print_instruction_message("Congratulations, adventurer!")
    print_instruction_message(" You stand before Waldo's cage.")
    print_instruction_message("To unlock the cage and free Waldo,")
    print_instruction_message("you must speak the magic word within 1 minute.")
    print()
    print_instruction_message(Fore.BLUE +
                              f"\nScrambled word:{Style.RESET_ALL}"
                              f"{Fore.YELLOW}{scrambled_word}"
                              + Style.RESET_ALL)
    start_time = time.time()
    end_time = start_time + 60
    while True:
        current_time = time.time()
        remaining_time = end_time - current_time
        if remaining_time >= 0:
            print(Fore.BLUE +
                  f"\nRemaining time: {Fore.RESET}{Fore.YELLOW} "
                  f"{int(remaining_time)} {Fore.RESET}{Fore.BLUE}seconds."
                  + Fore.RESET)
        if current_time >= end_time:
            print_validation_error("\nTime's up! "
                                   "The cage remains locked. "
                                   "Waldo remains trapped.")
            return False
        print_input_instructions("Enter the unscrambled magic word,"
                                 " use only letters from A to Z please.")
        player_guess = input_for_saving_info(
            "Enter the magic word: ").strip().lower()
        if not player_guess.isalpha():
            print_validation_error("\nInvalid characters entered. "
                                   "Please use only letters from A to Z.")
            continue
        if player_guess == unscrambled_word:
            print_empty_line_with_color()
            print_centered_text(
                "Good Job! You've spoken the magic word!", Fore.GREEN)
            print_empty_line_with_color()
            print()
            time.sleep(4)
            return True
        print_validation_error("\nIncorrect guess. Try again.")


# PLAY GAME FUNCTIION
def play_game():
    """
    Plays a multi-level game consisting of various challenges.

    Returns:
        None
    """
    start_time = time.time()  # Record the start time
    print()
    clear_screen()
    print_congratulations_message("WELCOME, ADVENTURER!")
    greet_player_and_explain_game()
    time.sleep(0.5)
    name, location = collect_player_info()
    if not play_password_level():
        print()
        print_separation_lines(Fore.RED)
        print_centered_text(
            "GAME OVER: The lock remains locked. Don't give up!"
            " Try again to save Waldo.", Fore.RED)
        print_separation_lines(Fore.RED)
        print()
        return
    if not play_riddle_level():
        print()
        print_separation_lines(Fore.RED)
        print_centered_text(
            "GAME OVER: The riddle remains unsolved."
            " Don't lose hope! Keep trying to save Waldo.", Fore.RED)
        print_separation_lines(Fore.RED)
        print()
        return
    if not play_rock_paper_scissors_level():
        print()
        print_separation_lines(Fore.RED)
        print_centered_text("GAME OVER: The enchanted knight,"
                            " All Mighty Paper O'Clipper,"
                            " proves too formidable for now."
                            " But fear not! Keep honing your skills"
                            " and challenge him again to continue"
                            " your quest to save Waldo.", Fore.RED)
        print_separation_lines(Fore.RED)
        print()
        return
    if not play_word_maze_level():
        print()
        print_separation_lines(Fore.RED)
        print_centered_text(
            "GAME OVER: The maze remains unconquered."
            " Don't give up! Keep striving to save Waldo.", Fore.RED)
        print_separation_lines(Fore.RED)
        print()
        return
    if not play_magic_word_level():
        print()
        print_separation_lines(Fore.RED)
        print_centered_text(
            "GAME OVER: The magic word eludes you for now."
            " But don't lose hope!"
            " Keep searching for way to reach Waldo's cage.", Fore.RED)
        print_separation_lines(Fore.RED)
        print()
        return
    end_time = time.time()
    time_taken = end_time - start_time
    record_score(name, location, time_taken)
    clear_screen()
    print_congratulations_message("Congratulations, brave adventurer! "
                                  "You've freed Waldo from his dungeon!")


# MAIN FUNCTION
def main():
    """
    Main function to orchestrate the game flow.
    """
    while True:
        play_game()
        print_instruction_message("VICTORY!")
        print_instruction_message(
            "With your keen eye and determination,"
            " you've freed Waldo from his elusive captivity.")
        print_instruction_message(
            "Now, he wanders the world at his leisure,"
            " appearing and disappearing as he pleases.")
        print_instruction_message(
            "But fear not, for the spirit of adventure lives on.")
        print_instruction_message(
            "For all those who yearn to seek, who long to wonder,"
            " who marvel at the mysteries of the world,")
        print_instruction_message(
            "Waldo may yet reveal himself again,"
            " in unexpected places and at unexpected times.")
        print_instruction_message(
            "So keep your eyes sharp and your heart open,")
        print_instruction_message(
            "For where there is wonder, there is Waldo.")
        print_congratulations_message("GAME OVER")
        while True:
            print()
            print_leaderboard(worksheet_scores)
            print_input_instructions("Do you want to play again? (yes/no)")
            restart = input_for_saving_info("Y or N: ").lower()
            if restart == "y":
                break
            if restart == "n":
                clear_screen()
                print("\n"*7)
                print_empty_line_with_color()
                print_centered_text("Thank you for saving Waldo and good"
                                    " luck in new adventures!", Fore.GREEN)
                print_empty_line_with_color()
                return
            print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == "__main__":
    main()
