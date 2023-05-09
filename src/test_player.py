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
