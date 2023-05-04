import guess


def test_random_word():
    word = guess.random_word(guess.word_list)
    assert len(word) == 5
    assert word.isalpha()
    assert word in guess.word_list


def test_check_guess_correct():
    assert guess.check_guess('apple', 'apple') == 'correct answer'


def test_check_guess_invalid():
    assert guess.check_guess('apple', 'appl') == 'input not valid'


def test_check_guess_continue():
    assert guess.check_guess(
        'party', 'apple') == [1, 1, 0, 0, 0]
    assert guess.check_guess(
        'apple', 'party') == [1, 1, 0, 0, 0]


def test_check_guess_duplicate():
    assert guess.check_guess(
        'eaten', 'lever') == [0, 1, 0, 2, 0]
    assert guess.check_guess(
        'apple', 'puple') == [1, 0, 2, 2, 2]
    assert guess.check_guess(
        'apple', 'puppy') == [1, 0, 2, 0, 0]
