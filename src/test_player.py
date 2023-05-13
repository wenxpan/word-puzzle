import pytest
from player import Player


@pytest.fixture
def player():
    return Player()


def test_get_spell_check_enabled(player):
    """Tested function: get_spell_check_enabled()
    Tests that the getter method is returning value as expected.
    It should return True as default value of spellcheck settings
    """
    assert player.get_spell_check_enabled() == True


def test_toggle_spell_check_enabled(player, capsys):
    """Tested function: toggle_spell_check_enabled()
    Test that spell check will be toggled 
    between ON and OFF"""
    # toggle from ON to OFF
    player.toggle_spell_check_enabled()
    captured = capsys.readouterr()
    assert player.get_spell_check_enabled() == False
    assert captured.out == "Spell check setting is now OFF.\n"

    # toggle from OFF to ON
    player.toggle_spell_check_enabled()
    captured = capsys.readouterr()
    assert player.get_spell_check_enabled() == True
    assert captured.out == "Spell check setting is now ON.\n"


def test_calculate_wins(player):
    """Tested function: calculate_wins()
    test to see that total play counts and wins
    are calculated correctly
    """
    records = [
        {"answer": "APPLE",
         "guess": ["PUPIL", "APPLY", "ORBIT"],
         "start_time": "16:40"},
        {"answer": "WATER",
         "guess": ["PUPIL", "APPLY", "ORBIT"],
         "start_time": "16:42"},
        {"answer": "ORBIT",
         "guess": ["PUPIL", "APPLY", "ORBIT"],
         "start_time": "16:40"},
    ]
    player.records = records
    assert player.calculate_wins() == "1/3"


def test_update_records(player):
    """Tested function: update_records()
    Test that data will be correctly appended to
    player records
    """
    # add first record
    answer = "APPLE"
    guessed_list = ["PUPIL", "APPLY", "ORBIT"]
    start_time = "16:40"
    player.update_records(answer, guessed_list, start_time)
    assert player.get_records() == [
        {"answer": "APPLE",
         "guess": ["PUPIL", "APPLY", "ORBIT"],
         "start_time": "16:40"}
    ]
    # add another record
    another_answer = "QUICK"
    another_guessed_list = ["PUPIL", "APPLY", "QUICK"]
    another_start_time = "16:41"
    player.update_records(
        another_answer, another_guessed_list, another_start_time)
    updated_records = [{"answer": "APPLE", "guess":
                        ["PUPIL", "APPLY", "ORBIT"],
                        "start_time": "16:40"},
                       {"answer": "QUICK", "guess":
                        ["PUPIL", "APPLY", "QUICK"],
                        "start_time": "16:41"}]
    assert player.get_records() == updated_records


def test_clear_records(player, monkeypatch):
    """Tested function: clear_records()
    test that clear_records will erase all records
    """
    # add some records to object
    monkeypatch.setattr('builtins.input', lambda _: "Y")
    answer = "APPLE"
    guessed_list = ["PUPIL", "APPLY", "ORBIT"]
    start_time = "16:40"
    player.update_records(answer, guessed_list, start_time)
    # ensure that current records holds value
    assert player.get_records() != []
    old_records = player.get_records()
    # test whether records become empty
    player.clear_records()
    assert player.get_records() == []
    assert player.get_records() != old_records
