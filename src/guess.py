import random

# open word list file and create a word list
with open('data/sgb-words-filtered.txt') as f:
    word_list = list(f.read().splitlines())


# return random word from word list
def random_word(words):
    return random.choice(words)


def check_guess(answer, guess):
    if guess == answer:
        result = 'correct answer'
    elif guess.isalpha() and len(guess) == 5:
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
    else:
        result = 'input not valid'
    return result

# answer = random_word(word_list)
# print(f'for dev: the answer is {answer}')
# guess = input("take a guess! ")


print(check_guess('party', 'apple'))
