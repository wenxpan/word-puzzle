import pytest
from player import Player, StartAgainException


@pytest.fixture
def player():
    return Player()


def test_get_spell_check_enabled(player):
    assert player.get_spell_check_enabled() == True


def test_toggle_spell_check_enabled_confirm(player, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'Y')
    with pytest.raises(StartAgainException):
        player.toggle_spell_check_enabled()
    captured = capsys.readouterr()
    assert player.get_spell_check_enabled() == False
    assert captured.out == 'Spell check setting is now off.\n'


def test_toggle_spell_check_enabled_cancel(player, monkeypatch, capsys):
    monkeypatch.setattr('builtins.input', lambda _: 'N')
    player.toggle_spell_check_enabled()
    captured = capsys.readouterr()
    assert player.get_spell_check_enabled() == True
    assert captured.out == 'Back to the main game.\n'


def test_get_save_data(player):
    assert player.get_save_data() == []


def test_update_save_data(player):
    answer = 'APPLE'
    guessed_list = ["PUPIL", "APPLY", "ORBIT"]
    start_time = '16:40'
    end_time = '16:41'
    player.update_save_data(answer, guessed_list, start_time, end_time)
    assert player.get_save_data() == [
        {'answer': 'APPLE', 'guess': ["PUPIL", "APPLY", "ORBIT"], 'time': ['16:40', '16:41']}]

    another_answer = "QUICK"
    another_guessed_list = ["PUPIL", "APPLY", "QUICK"]
    another_start_time = '16:41'
    another_end_time = '16:42'
    player.update_save_data(
        another_answer, another_guessed_list, another_start_time, another_end_time)
    assert player.get_save_data() == [{'answer': 'APPLE', 'guess': ["PUPIL", "APPLY", "ORBIT"], 'time': ['16:40', '16:41']}, {
        'answer': "QUICK", 'guess': ["PUPIL", "APPLY", "QUICK"], "time": ['16:41', '16:42']}]
