import guess
import pytest


def test_get_random_word_valid():
    """Tested function: get_random_word()
    test that a random word can be drawn from a valid word list
    """
    word_list = ["apple", "water", "faint", "quiet", "33", "a"]
    word = guess.get_random_word(word_list)
    assert word.isalpha()
    assert word.lower() in [x.lower() for x in word_list]


def test_get_random_word_empty():
    """Tested function: get_random_word()
    test that empty list will display error message
    """
    word_list = []
    with pytest.raises(KeyboardInterrupt):
        guess.get_random_word(word_list)


def test_get_random_word_invalid():
    """Tested function: get_random_word()
    test that when there are no English words longer than
    2 characters in the word list, error raises
    """
    word_list = ["a", "22", "3"]
    with pytest.raises(KeyboardInterrupt):
        guess.get_random_word(word_list)


def test_check_input_word_valid(monkeypatch):
    """Tested function: check_input_word()
    check that valid input word will be returned in uppercase
    """
    monkeypatch.setattr("builtins.input", lambda _: "apple")
    assert guess.check_input_word([], 5) == "APPLE"


def test_check_input_word_invalid(monkeypatch, capsys):
    """Tested function: check_input_word()
    check that invalid input is warned and 
    correct input is captured
    """
    inputs = iter(["33", "apple"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = guess.check_input_word([], 5)
    captured = capsys.readouterr()
    assert "Input not valid" in captured.out
    assert result == "APPLE"


def test_check_input_word_guessed(monkeypatch, capsys):
    """Tested function: check_input_word()
    check that guessed input is not returned and 
    warning message is captured
    """
    inputs = iter(["apple", "pupil"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = guess.check_input_word(["APPLE"], 5)
    captured = capsys.readouterr()
    assert "You already tried this word!" in captured.out
    assert result == "PUPIL"


def test_check_input_word_misspelled(monkeypatch, capsys):
    """Tested function: check_input_word()
    check that when spellcheck is on, misspelled
    word is not accepted and warning message is displayed
    """
    inputs = iter(["appli", "apply"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))
    result = guess.check_input_word([], 5)
    captured = capsys.readouterr()
    assert "not in the dictionary" in captured.out
    assert result == "APPLY"


def test_check_exact_match():
    """Tested function: check_exact_match()
    check case-insensitive words will be considered as 
    exact match
    """
    assert guess.check_exact_match("apple", "APPLE") == True
    assert guess.check_exact_match("apple", "Apple") == True
    assert guess.check_exact_match("apple", "apple") == True
    assert guess.check_exact_match("apple", "puple") == False


def test_check_letter_normal():
    """Tested function: check_letter()
    test that correct array will be returned to indicate 
    correct(2), misplaced(1) and wrong(0) letters
    """
    assert guess.check_letter(
        "party", "apple", 5) == [1, 1, 0, 0, 0]
    assert guess.check_letter(
        "apple", "party", 5) == [1, 1, 0, 0, 0]


def test_check_letter_duplicate():
    """Tested function: check_letter()
    Test some more complex cases, where there are duplicate
    letters. For example for the answer "eaten", if guess is
    "lever", the first "e" will be misplaced, while the second
    "e" will be correct. The order of the results must not be
    swapped.
    In answer "apple" and guess "puppy", the third "p" will be
    wrong because there are already two "p"s.
    """
    assert guess.check_letter(
        "eaten", "lever", 5) == [0, 1, 0, 2, 0]
    assert guess.check_letter(
        "apple", "puple", 5) == [1, 0, 2, 2, 2]
    assert guess.check_letter(
        "apple", "puppy", 5) == [1, 0, 2, 0, 0]
    assert guess.check_letter(
        "tight", "fight", 5) == [0, 2, 2, 2, 2]
    assert guess.check_letter(
        "elude", "ledge", 5) == [1, 1, 1, 0, 2]


def test_highlight_letter():
    """tested function: highlight_letter()
    test that it will return text with correct format
    expected output: green when result is 2, 
    yellow when result is 1, white(grey) when 
    result is 0
    """
    assert guess.highlight_letter(
        "L", 2) == ("[bold black on bright_green]"
                    " L [/bold black on bright_green]")
    assert guess.highlight_letter(
        "A", 1) == ("[bold black on bright_yellow]"
                    " A [/bold black on bright_yellow]")
    assert guess.highlight_letter(
        "O", 0) == "[bold black on white] O [/bold black on white]"
