import guess


def test_random_word():
    word = guess.get_random_word(guess.word_list)
    assert word.isalpha()
    assert word in guess.word_list


def test_check_input_word_correct(monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'apple')
    assert guess.check_input_word([], 5) == 'APPLE'


def test_check_input_word_invalid(monkeypatch, capsys):
    inputs = iter(['33', 'apple'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = guess.check_input_word([], 5)
    captured = capsys.readouterr()
    assert captured.out == 'Input not valid. Please enter a 5-letter English word\n\n'
    assert result == 'APPLE'


def test_check_input_word_guessed(monkeypatch, capsys):
    inputs = iter(['apple', 'pupil'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = guess.check_input_word(['APPLE'], 5)
    captured = capsys.readouterr()
    assert captured.out == 'You already guessed this word!\n\n'
    assert result == 'PUPIL'


def test_check_input_word_incorrect(monkeypatch, capsys):
    inputs = iter(['appli', 'apply'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    result = guess.check_input_word([], 5)
    captured = capsys.readouterr()
    assert captured.out == 'Word not found in dictionary.\n\n'
    assert result == 'APPLY'


def test_check_exact_match():
    assert guess.check_exact_match('apple', 'APPLE') == True
    assert guess.check_exact_match('apple', 'Apple') == True
    assert guess.check_exact_match('apple', 'apple') == True
    assert guess.check_exact_match('apple', 'puple') == False


def test_check_letter_normal():
    assert guess.check_letter(
        'party', 'apple', 5) == [1, 1, 0, 0, 0]
    assert guess.check_letter(
        'apple', 'party', 5) == [1, 1, 0, 0, 0]


def test_check_letter_duplicate():
    assert guess.check_letter(
        'eaten', 'lever', 5) == [0, 1, 0, 2, 0]
    assert guess.check_letter(
        'apple', 'puple', 5) == [1, 0, 2, 2, 2]
    assert guess.check_letter(
        'apple', 'puppy', 5) == [1, 0, 2, 0, 0]
    assert guess.check_letter(
        'tight', 'fight', 5) == [0, 2, 2, 2, 2]


def test_highlight_letter():
    assert guess.highlight_letter(
        'L', 2) == '[bold black on bright_green] L [/bold black on bright_green]'
    assert guess.highlight_letter(
        'A', 1) == '[bold black on bright_yellow] A [/bold black on bright_yellow]'
    assert guess.highlight_letter(
        'O', 0) == '[bold black on white] O [/bold black on white]'


def test_highlight_word():
    assert guess.highlight_word(
        'PUPLE', [1, 0, 2, 2, 2]
    ) == "[bold black on bright_yellow] P [/bold black on bright_yellow][bold black on white] U [/bold black on white][bold black on bright_green] P [/bold black on bright_green][bold black on bright_green] L [/bold black on bright_green][bold black on bright_green] E [/bold black on bright_green]\n"
