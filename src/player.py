class StartAgainException(Exception):
    pass


# class with game settings
class Player():
    def __init__(self):
        self.spell_check_enabled = True

    # get current spell check state

    def get_spell_check_enabled(self):
        return self.spell_check_enabled

    # toggle spell check on or off

    def toggle_spell_check_enabled(self):
        confirmed = input(
            f"Spell check setting is currently {'on' if self.spell_check_enabled else 'off'}. Toggling spell check will start a new game. \nEnter 'Y' to confirm. \nEnter any other button to exit setting.\n")
        if confirmed.upper() == 'Y':
            self.spell_check_enabled = not self.spell_check_enabled
            print(
                f"Spell check setting is now {'on' if self.spell_check_enabled else 'off'}")
            raise StartAgainException
        else:
            print('Back to the main game.')
