import random
from rich import print

# open word list file and create a word list
with open('data/sgb-words-filtered.txt') as f:
    word_list = list(f.read().splitlines())


# return random word from word list
def get_random_word(words):
    return random.choice(words)


# check the user input is a valid 5 letter word and not guessed
def take_input(guessed_list):
    while True:
        guess = input('Take a guess: ').upper()
        if guess in guessed_list:
            print('You already guessed this word!')
        elif guess.isalpha() and len(guess) == 5:
            # return in uppercase
            return guess
        else:
            print('Input not valid! Please enter a 5-letter word')


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
            result[index] = 1
            answer_list[answer_list.index(letter)] = 0
    return result


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
    return f"[{colors[color]}] {letter} [/{colors[color]}]"


def highlight_word(guess, result_list):
    message = ''
    for index, result in enumerate(result_list):
        message += highlight_letter(guess[index], result)
    return message


# main play
def play():
    answer = get_random_word(word_list).upper()
    guessed_list = []
    print(f'for dev: word is {answer}')
    for i in range(1, 7, 1):
        print(f'Round: {i}/6')
        guess = take_input(guessed_list)
        guessed_list.append(guess)
        if check_exact_match(answer, guess):
            print('You won!')
            break
        else:
            print(check_letter(answer, guess))
    print(f'You lose! The answer is {answer}')


# print(f"[{colors['green']}] A [/{colors['green']}][{colors['yellow']}] P [{colors['yellow']}][{colors['yellow']}] P [{colors['yellow']}][{colors['grey']}] L [{colors['grey']}][{colors['grey']}] E [{colors['grey']}]")
