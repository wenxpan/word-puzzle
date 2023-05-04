import guess


def test_random_word():
    word = guess.random_word(guess.word_list)
    assert len(word) == 5
    assert word.isalpha()
    assert word in guess.word_list
