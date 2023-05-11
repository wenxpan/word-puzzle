import random
from rich import print
from rich.prompt import Prompt
from datetime import datetime
from spellchecker import SpellChecker
from player import create_player
from story import print_welcome

player = create_player()


class StartAgainException(Exception):
    pass


# open word list file and create a word list
with open(player.get_list_path()) as f:
    word_list = list(f.read().splitlines())


# return random word from word list
def get_random_word(words):
    return random.choice(words)


# take user input and validate if it is special command; if not, return the input value
def take_input(prompt):
    user_input = input(prompt)

    # quit game
    if user_input.upper() == '\\Q':
        raise KeyboardInterrupt

    # restart game
    elif user_input.upper() == '\\R':
        raise StartAgainException

    else:
        return user_input


# check the user guess is a valid 5 letter word and not already guessed
def check_input_word(guessed_list, word_length):
    # repeatedly ask for input until it receives a valid word for analysis
    while True:
        # convert to uppercase to compare with previous results
        guess = take_input(f'Take a guess: ({word_length} letters)\n').upper()
        spell = SpellChecker()
        misspelled = bool(spell.unknown([guess]))
        # check if word is already guessed
        if guess in guessed_list:
            print('You already guessed this word!\n')
        # check if input is an English word and 5 letters long
        elif not guess.isalpha() or len(guess) != word_length:
            print(
                f'Input not valid. Please enter a {word_length}-letter English word\n')
        # if spell check enabled, check if it is misspelled
        elif player.get_spell_check_enabled() and misspelled:
            print(
                f'Friendly Fairy warns you that the word is not in the dictionary. Try another word!\n')
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
            # correct letter will be reset to 0 in the answer list to avoid duplicate match
            answer_list[index] = 0
    # round 2: check for misplaced letters
    for index, letter in enumerate(guess):
        if letter in answer_list:
            # avoid overwriting correct result
            if result[index] != 2:
                result[index] = 1
                # find the index of answer letter and reset that to 0 to avoid duplicate match
                answer_list[answer_list.index(letter)] = 0
    # return result array ready for highlighting
    return result


# highlight letter based on analysis
def highlight_letter(letter, result):
    # define coloring in rich
    colors = {'green': 'bold black on bright_green',
              'yellow': 'bold black on bright_yellow', 'grey': 'bold black on white'}
    color = ''
    # grey for wrong letter, yellow for misplaced letter, green for correct letter
    match result:
        case 0:
            color = 'grey'
        case 1:
            color = 'yellow'
        case 2:
            color = 'green'
    message = f"[{colors[color]}] {letter} [/{colors[color]}]"
    return message


# highlight word based on analysis
def highlight_word(guess, result_list):
    message = ''
    for index, result in enumerate(result_list):
        message += highlight_letter(guess[index], result)
    message += '\n'
    return message


# one round of play
def play_once():
    # draw a random word from list
    answer = get_random_word(word_list[0:500]).upper()
    word_length = len(answer)
    # set a list of guessed words
    guessed_list = []
    # set initial message
    message = '\n'
    num_chances = player.get_num_chances()
    print(f'****for dev: word is {answer}****')
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # start_time = datetime.now()
    # loop 6 rounds of guess
    for i in range(1, num_chances+1, 1):
        print(
            f"==========================================\n(Round: {i}/{num_chances}              SpellCheck: {player.display_spell_check_status()})\n")
        # get a valid word for analysis
        guess = check_input_word(guessed_list, word_length)
        # add the word to guessed list
        guessed_list.append(guess)
        # if guess matches answer, show winning message and end the loop
        if check_exact_match(answer, guess):
            print('You won!')
            break
        # if not won, compare and show result
        else:
            result = check_letter(answer, guess, word_length)
            message += highlight_word(guess, result)
            print(message)
    # after loop ends and the user has not won, display losing message
    else:
        print(f'You lose! The answer is {answer}')
    # check how the user would like to continue
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # end_time = datetime.now()
    player.update_records(answer, guessed_list, start_time, end_time)
    player.save_data()
    continue_prompt = take_input(
        'Progress auto saved. \nEnter "\\s" to save a separate record and start a new game.\nEnter "\\q" to quit. Enter any other button to start a new game.\n').upper()
    if continue_prompt == "\\S":
        player.export_records_latest()


def play_loop():
    # display welcome message
    player.load_data()
    print_welcome(player.get_name(), player.get_num_chances())
    try:
        # main play loop
        while True:
            try:
                play_once()
            # restart the game when user uses \r
            except StartAgainException:
                continue
    # exit the game when user uses \q
    except KeyboardInterrupt:
        print('Thank you for playing. See you next time!')


if __name__ == '__main__':
    play_loop()
