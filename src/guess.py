import random

# open word list file and create a word list
with open('data/sgb-words-filtered.txt') as f:
    word_list = list(f.read().splitlines())


# return random word from word list
def random_word(words):
    return random.choice(words)


random_word(word_list)
