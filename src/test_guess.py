import guess


def test_random_word():
    word = guess.get_random_word(guess.word_list)
    assert len(word) == 5
    assert word.isalpha()
    assert word in guess.word_list


def test_take_input(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 'appl')
    monkeypatch.setattr('builtins.input', lambda _: 'apple')
    assert guess.take_input() == 'APPLE'

    monkeypatch.setattr('builtins.input', lambda _: 'puple')
    assert guess.take_input() == 'PUPLE'

    monkeypatch.setattr('builtins.input', lambda _: '11')
    monkeypatch.setattr('builtins.input', lambda _: '111')
    monkeypatch.setattr('builtins.input', lambda _: 'puppy')
    assert guess.take_input() == 'PUPPY'


def test_check_exact_match():
    assert guess.check_exact_match('apple', 'APPLE') == True
    assert guess.check_exact_match('apple', 'Apple') == True
    assert guess.check_exact_match('apple', 'apple') == True
    assert guess.check_exact_match('apple', 'puple') == False


def test_check_letter_normal():
    assert guess.check_letter(
        'party', 'apple') == [1, 1, 0, 0, 0]
    assert guess.check_letter(
        'apple', 'party') == [1, 1, 0, 0, 0]


def test_check_letter_duplicate():
    assert guess.check_letter(
        'eaten', 'lever') == [0, 1, 0, 2, 0]
    assert guess.check_letter(
        'apple', 'puple') == [1, 0, 2, 2, 2]
    assert guess.check_letter(
        'apple', 'puppy') == [1, 0, 2, 0, 0]