import random
from rich import print
from spellchecker import SpellChecker
from player import create_player
from story import print_welcome, hint_messages, win_messages, lose_messages
from helper import StartAgainException, current_time_string, print_red

# create a player object
player = create_player()


# open word list file and create a word list
def get_word_list():
    try:
        with open(player.get_list_path()) as f:
            word_list = list(f.read().splitlines())
        return word_list
    except FileNotFoundError:
        print_red(
            "Word list not found! "
            "Go back to player settings and confirm you have the right list selected.")
        raise KeyboardInterrupt


# return random word in upper case from word list
def get_random_word(words):
    for i in words:
        word = random.choice(words).upper()
        # check if the random word is longer than 2 characters and contains alphabet only
        if len(word) >= 3 and word.isalpha():
            return word
    # if unable to find a matching word, return error message and exit the game
    else:
        print_red("\nUh oh! Looks like no word can be drawn from the selected word list.\n"
                  "The list needs to contain words with more than 2 characters.\n"
                  "Select another word list in player settings and come back later.")
        raise KeyboardInterrupt


# take user input and validate if it is special command; if not, return the input value
def take_input(prompt):
    user_input = input(prompt)

    # quit game
    if user_input.upper() == "\\Q":
        raise KeyboardInterrupt

    # restart game
    elif user_input.upper() == "\\R":
        raise StartAgainException

    else:
        return user_input


# check the user guess is a valid English word that
# matches the answer length and not already guessed
def check_input_word(guessed_list, word_length):
    # repeatedly ask for input until it receives a valid word for analysis
    while True:
        # convert to uppercase to compare with previous results
        guess = take_input(f"Take a guess: ({word_length} letters)\n").upper()
        # spellcheck the guess
        spell = SpellChecker()
        misspelled = bool(spell.unknown([guess]))
        # check if word is already guessed
        if guess in guessed_list:
            print("You already tried this word!\n")
        # check if input is an English word and the same length as answer
        elif not guess.isalpha() or len(guess) != word_length:
            print(
                f"Input not valid. "
                "Please enter a {word_length}-letter English word\n")
        # if spell check enabled, check if it is misspelled
        elif player.get_spell_check_enabled() and misspelled:
            print(
                "Friendly Fairy warns you that the word "
                "is [bold]not in the dictionary[/bold]."
                "Try another word!\n")
        # return guessed word if all validation passed
        else:
            return guess


# check if the input is the same as answer
def check_exact_match(answer, guess):
    if guess.upper() == answer.upper():
        return True
    else:
        return False


# analyse user input and compare each letter
def check_letter(answer, guess, word_length):
    # set up result array, 0 = wrong, 1 = misplaced, 2 = correct
    result = [0] * word_length
    # convert answer string to a list, to compare both letter and order
    answer_list = list(answer)
    # round 1: check for correct letters
    for index, letter in enumerate(guess):
        if letter == answer_list[index]:
            result[index] = 2
            # correct letter will be reset to 0
            # in the answer list to avoid duplicate match
            answer_list[index] = 0
    # round 2: check for misplaced letters
    for index, letter in enumerate(guess):
        if letter in answer_list:
            # avoid overwriting correct result
            if result[index] != 2:
                result[index] = 1
                # find the index of answer letter and
                # reset that to 0 to avoid duplicate match
                answer_list[answer_list.index(letter)] = 0
    # return result array ready for highlighting
    return result


# highlight letter based on analysis
def highlight_letter(letter, result):
    # define coloring in rich
    colors = {"green": "bold black on bright_green",
              "yellow": "bold black on bright_yellow",
              "grey": "bold black on white"}
    color = ""
    # grey for wrong letter,
    # yellow for misplaced letter,
    # green for correct letter
    match result:
        case 0:
            color = "grey"
        case 1:
            color = "yellow"
        case 2:
            color = "green"
    highlighted_letter = (
        f"[{colors[color]}] {letter} [/{colors[color]}]"
    )
    return highlighted_letter


# highlight word based on analysis
def highlight_word(guess, result_list):
    highlighted_line = ""
    # loop through each letter
    for index, result in enumerate(result_list):
        highlighted_line += highlight_letter(guess[index], result)
    highlighted_line += "\n"
    return highlighted_line


# one round of play
def play_once():
    # draw a random word from list
    word_list = get_word_list()
    answer = get_random_word(word_list)
    # get length of the word
    word_length = len(answer)
    # set a list of guessed words
    guessed_list = []
    # set initial hint message
    hints = "\n"
    # get the total number of chances
    num_chances = player.get_num_chances()
    print(f"****for dev: word is {answer}****")
    # return start time in given format
    start_time = current_time_string("%Y-%m-%d %H:%M:%S")
    # loop guesses based on number of chances set
    for i in range(1, num_chances+1, 1):
        print(
            f"==========================================\n(Round: {i}/{num_chances}"
            f"              SpellCheck: {player.display_spell_check_status()})\n")
        # get a valid word for analysis
        guess = check_input_word(guessed_list, word_length)
        # add the word to guessed list
        guessed_list.append(guess)
        # if guess matches answer, show winning message and end the loop
        if check_exact_match(answer, guess):
            print(
                "[italic green]The spell works! "
                f"{random.choice(win_messages)}[/italic green]")
            break
        # if not won, compare and show hints
        else:
            result = check_letter(answer, guess, word_length)
            hints += highlight_word(guess, result)
            print(
                f"\n[italic]{random.choice(hint_messages)}[/italic]\n{hints}")
    # if loop ends without breaking(i.e. the user has not won), display losing message
    else:
        print(
            "[italic purple]You've run out of chances! "
            f"The secret word is [bold]{answer}[/bold].\n"
            f"{random.choice(lose_messages)}[/italic purple]\n"
        )
    # store current record in player object and export as json file
    player.update_records(answer, guessed_list, start_time)
    player.save_data()
    # display prompt to continue/save/quit the game
    continue_prompt = take_input(
        "\n**Progress auto saved. Head to user_data/save_data.json to copy backups.**\n"
        "Enter '\\s' to export current round as txt and start a new game.\n"
        "Enter '\\q' to quit.\n"
        "Enter any other button to start a new game.\n")
    # if user types \s, export record of the latest play
    if continue_prompt.upper() == "\\S":
        player.export_records_latest()


def play_loop():
    # display welcome message
    print_welcome(player.get_name(), player.get_num_chances())
    try:
        # main play loop
        while True:
            try:
                play_once()
            # restart the game when user uses \r
            except StartAgainException:
                continue
    # exit the game when user raises keyboard interrupt (ctrl+c and \q)
    except KeyboardInterrupt:
        print(
            "[italic blue]Mr. Python seems disappointed. "
            "He hopes to see you soon![/italic blue]")


if __name__ == "__main__":
    play_loop()
