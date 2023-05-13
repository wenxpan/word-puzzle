import pytest
from player import Player
from guess import StartAgainException


@pytest.fixture
def player():
    return Player()


def test_get_spell_check_enabled(player):
    assert player.get_spell_check_enabled() == True


def test_toggle_spell_check_enabled_confirm(player, capsys):
    player.toggle_spell_check_enabled()
    captured = capsys.readouterr()
    assert player.get_spell_check_enabled() == False
    assert captured.out == 'Spell check setting is now OFF.\n'


def test_get_records(player):
    assert player.get_records() == []


def test_update_records(player):
    answer = 'APPLE'
    guessed_list = ["PUPIL", "APPLY", "ORBIT"]
    start_time = '16:40'
    player.update_records(answer, guessed_list, start_time)
    assert player.get_records() == [
        {'answer': 'APPLE', 'guess': ["PUPIL", "APPLY", "ORBIT"], 'start_time': '16:40'}]

    another_answer = "QUICK"
    another_guessed_list = ["PUPIL", "APPLY", "QUICK"]
    another_start_time = '16:41'
    player.update_records(
        another_answer, another_guessed_list, another_start_time)
    updated_records = [{'answer': 'APPLE', 'guess': ["PUPIL", "APPLY", "ORBIT"], 'start_time': '16:40'}, {
        'answer': "QUICK", 'guess': ["PUPIL", "APPLY", "QUICK"], "start_time": '16:41'}]
    assert player.get_records() == updated_records


def test_set_num_chances_number(player, monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: '30')
    assert player.set_num_chances() == 30
