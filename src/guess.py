import random
from rich import print
from datetime import datetime
from spellchecker import SpellChecker

# open word list file and create a word list
with open('data/sgb-words-filtered.txt') as f:
    word_list = list(f.read().splitlines())


def welcome():
    print("""   ---------------------------------WELCOME---------------------------------
    Welcome to the game! 
    You will have 6 chances to guess a 5-letter word.
    Type '\\q' to exit the app anytime. Type '\\r' to start a new game.
    Type '\\sc' to toggle on and off spell checks
   -------------------------------------------------------------------------""")

# return random word from word list


def get_random_word(words):
    return random.choice(words)


class StartAgainException(Exception):
    pass


class ToggleSpellCheckException(Exception):
    pass


def take_input(prompt):
    user_input = input(prompt)

    if user_input.upper() == '\\Q':
        raise KeyboardInterrupt

    elif user_input.upper() == '\\R':
        raise StartAgainException

    elif user_input.upper() == '\\SC':
        raise ToggleSpellCheckException

    return user_input


# check the user input is a valid 5 letter word and not guessed
def check_input_word(guessed_list, spellcheck):
    while True:
        # convert to uppercase to compare with previous results
        guess = take_input('Take a guess: ').upper()
        spell = SpellChecker()
        misspelled = bool(spell.unknown([guess]))
        if guess in guessed_list:
            print('You already guessed this word!\n')
        elif not guess.isalpha() or len(guess) != 5:
            print('Input not valid. Please enter a 5-letter English word\n')
        elif spellcheck and misspelled:
            print(
                f'Word not found in dictionary.\n')
        else:
            return guess


# check if the input is correct
def check_exact_match(answer, guess):
    if guess.upper() == answer.upper():
        return True
    return False


# analyse user input and compare each letter
def check_letter(answer, guess):
    # check each letter
    result = [0, 0, 0, 0, 0]
    answer_list = list(answer)
    # check for correct letters; compared letters will be removed in the answer list to avoid duplicates
    for index, letter in enumerate(guess):
        if letter == answer_list[index]:
            result[index] = 2
            answer_list[index] = 0
    # check for misplaced letters
    for index, letter in enumerate(guess):
        if letter in answer_list:
            if result[index] != 2:
                result[index] = 1
                answer_list[answer_list.index(letter)] = 0
    return result


# highlight letter based on analysis


def highlight_letter(letter, result):
    colors = {'green': 'bold black on bright_green',
              'yellow': 'bold black on bright_yellow', 'grey': 'bold black on white'}
    color = ''
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


# export record as txt file
def export_record(guessed_list, answer, name):
    with open(f'user_data/record_{name}.txt', 'w') as f:
        f.write('=================\n')
        for word in guessed_list:
            f.write(f"  | {' '.join(word)} |  \n")
        f.write('=================\n')
        f.write(f'CORRECT WORD IS: {answer}\n')
    print(
        f"Record saved! You can find it in user_data/record/record_{name}.txt")


def play_once():
    answer = get_random_word(word_list[0:500]).upper()
    guessed_list = []
    message = '\n'
    print(f'****for dev: word is {answer}****')
    spell_check_setting = True
    for i in range(1, 7, 1):
        print(f'Round: {i}/6')
        try:
            guess = check_input_word(guessed_list, spell_check_setting)
        except ToggleSpellCheckException:
            spell_check_setting = not spell_check_setting
            print(
                f"Spell check setting now {'on' if spell_check_setting else 'off'}")
            guess = check_input_word(guessed_list, spell_check_setting)
        guessed_list.append(guess)
        if check_exact_match(answer, guess):
            print('You won!')
            break
        else:
            result = check_letter(answer, guess)
            message += highlight_word(guess, result)
            print(message)
    else:
        print(f'You lose! The answer is {answer}')
    if take_input('Enter "\\s" to save a record.\n').upper() == "\\S":
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        export_record(guessed_list, answer, current_time)


def play_loop():
    welcome()
    try:
        while True:
            try:
                play_once()
                if take_input('Enter "\\r" to play again. Enter any other button to quit the game.\n').upper() != "\\R":
                    raise KeyboardInterrupt
            except StartAgainException:
                continue
    except KeyboardInterrupt:
        print('Thank you for playing. See you next time!')


if __name__ == '__main__':
    play_loop()
