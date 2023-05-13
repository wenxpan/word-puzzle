import random
from rich import print
from spellchecker import SpellChecker
from player import create_player
from story import (print_welcome, hint_messages,
                   win_messages, lose_messages)
from helper import (StartAgainException, current_time_string,
                    print_red, highlight_text)


def get_word_list(file_path):
    """opens player's selected txt file and 
    create a word list from it
    """
    try:
        with open(file_path) as f:
            word_list = list(f.read().splitlines())
        return word_list
    except FileNotFoundError:
        print_red(
            "Word list not found! "
            "Go back to player settings and "
            "confirm you have the right list selected.")
        raise KeyboardInterrupt


def get_random_word(words):
    """return random word in upper case from word list"""
    for i in words:
        word = random.choice(words).upper()
        # check if the random word is longer than
        # 2 characters and contains alphabet only
        if len(word) >= 3 and word.isalpha():
            return word
    # if unable to find a matching word,
    # return error message and exit the game
    else:
        print_red("\nUh oh! Looks like no word can be drawn from "
                  "the selected word list.\nThe list needs to "
                  "contain words with more than 2 characters.\n"
                  "Select another word list in player settings "
                  "and come back later.")
        raise KeyboardInterrupt


def take_input(prompt):
    """take user input and validate if it is special command;
    if valid, return the input value
    if special command, raise error for program to catch later
    """
    user_input = input(prompt)

    # quit game
    if user_input.upper() == "\\Q":
        raise KeyboardInterrupt

    # restart game
    elif user_input.upper() == "\\R":
        raise StartAgainException

    else:
        return user_input


def check_input_word(spell_check_enabled, guessed_list, word_length):
    """check the user guess is an English word 
    that matches the answer length and not already guessed
    once user input is valid, return the value for analysis
    """
    # repeatedly ask for input until
    # it receives a valid word for analysis
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
                f"Please enter a {word_length}-letter English word\n")
        # if spell check enabled, check if it is misspelled
        elif spell_check_enabled and misspelled:
            print(
                "Friendly Fairy warns you that the word "
                "is [bold]not in the dictionary[/bold]. "
                "Try another word!\n")
        # return guessed word if all validation passed
        else:
            return guess


def check_exact_match(answer, guess):
    """check if the user's guess is the same as answer"""
    if guess.upper() == answer.upper():
        return True
    else:
        return False


def check_letter(answer, guess, word_length):
    """analyse user's guess and compare letter by letter"""
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


def highlight_letter(letter, result):
    """return highlighted letter based on analysed result"""
    # add space before and after the letter for better visuals
    text = f" {letter} "
    # set color to be used
    fore_color = "bold black"
    bg_color = ""
    match result:
        case 0:
            # grey for wrong letter
            bg_color = "white"
        case 1:
            # yellow for misplaced letter
            bg_color = "bright_yellow"
        case 2:
            # green for correct letter
            bg_color = "bright_green"
    # use helper function to highlight the text
    highlighted_letter = highlight_text(text, fore_color, bg_color)
    return highlighted_letter


def highlight_word(guess, result_list):
    """return highlighted word based on analysis"""
    # add spaces (margin) to the screen left
    highlighted_line = "      "
    # loop through each letter and highlight
    for index, result in enumerate(result_list):
        highlighted_line += highlight_letter(guess[index], result)
    highlighted_line += "\n"
    return highlighted_line


def play_once(player, word_list):
    """Process for one round of play
    1. generate word list and random word
    2. set up relevant info
    3. start loop: ask for user input
    4. validate and analyse input
    5. show ending message based on result
    6. auto save data
    7. ask if user wants to export records and start again
    """
    # draw a random word from list
    answer = get_random_word(word_list)
    # get length of the word
    word_length = len(answer)
    # set a list of guessed words
    guessed_list = []
    # set initial hint message
    hints = "\n"
    # get the total number of chances
    num_chances = player.get_num_chances()
    # get spell check status
    spell_check_enabled = player.get_spell_check_enabled()
    # return start time in given format
    start_time = current_time_string("%Y-%m-%d %H:%M:%S")
    # loop guesses based on number of chances set
    for i in range(1, num_chances+1, 1):
        print(
            "==========================================\n"
            f"(Round: {i}/{num_chances}"
            "              SpellCheck: "
            f"{player.display_spell_check_status()})\n")
        # get a valid word for analysis
        guess = check_input_word(
            spell_check_enabled, guessed_list, word_length)
        # add the word to guessed list
        guessed_list.append(guess)
        # if guess matches answer, show win message and end loop
        if check_exact_match(answer, guess):
            print(
                "[italic reverse]The spell works! "
                f"{random.choice(win_messages)}[/italic reverse]")
            break
        # if not won, compare and show hints
        else:
            result = check_letter(answer, guess, word_length)
            hints += highlight_word(guess, result)
            print(
                f"\n[italic]{random.choice(hint_messages)}[/italic]\n{hints}")
    # if loop ends without breaking, display losing message
    else:
        print(
            "[italic reverse]You've run out of chances! "
            f"The secret word is [bold]{answer}[/bold].\n"
            f"{random.choice(lose_messages)}[/italic reverse]\n"
        )
    # store current record in player object and export as json file
    player.update_records(answer, guessed_list, start_time)
    player.save_data()
    # display prompt to continue/save/quit the game
    continue_prompt = take_input(
        "\n**Progress auto saved. Head to user_data/save_data.json "
        "to copy backups.**\n"
        "Enter '\\s' to export current round as txt and start a new game.\n"
        "Enter '\\q' to quit.\n"
        "Enter any other button to start a new game.\n")
    # if user types \s, export record of the latest play
    if continue_prompt.upper() == "\\S":
        player.export_records_latest()


def play_loop():
    """Main play"""
    player = create_player()
    # display welcome message
    player_name = player.get_name()
    player_chances = player.get_num_chances()
    print_welcome(player_name, player_chances)
    try:
        # generate word list based on txt file
        list_path = player.get_list_path()
        word_list = get_word_list(list_path)
        # main play loop
        while True:
            try:
                play_once(player, word_list)
            # when user uses \r, raise exception to jump out
            # of current play round and restart from the beginning
            except StartAgainException:
                continue
    # exit the game when user raises keyboard interrupt (ctrl+c and \q)
    except KeyboardInterrupt:
        print(
            "[reverse]Mr. Python seems disappointed. "
            "He hopes to see you soon![/reverse]")
