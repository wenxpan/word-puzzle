import random

# open word list file and create a word list
with open('data/sgb-words-filtered.txt') as f:
    word_list = list(f.read().splitlines())


# return random word from word list
def random_word(words):
    return random.choice(words)


# check the user input is a valid 5 letter word
def validate_input(guess):
    if guess.isalpha() and len(guess) == 5:
        return True
    return False


# check if the input is correct
def check_exact_match(answer, guess):
    if guess.lower() == answer.lower():
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
