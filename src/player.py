class StartAgainException(Exception):
    pass


# class with game settings
class Player():
    def __init__(self, name):
        self.spell_check_enabled = True
        self.save_data = []
        self.name = name

    # get current spell check state
    def get_spell_check_enabled(self):
        return self.spell_check_enabled

    def display_spell_check_status(self):
        return 'ON' if self.spell_check_enabled else 'OFF'

    # toggle spell check on or off
    def toggle_spell_check_enabled(self):
        confirmed = input(
            f"Spell check setting is currently {self.display_spell_check_status()}. Toggling spell check will start a new game. \nEnter 'Y' to confirm. \nEnter any other button to exit setting.\n")
        if confirmed.upper() == 'Y':
            self.spell_check_enabled = not self.spell_check_enabled
            print(
                f"Spell check setting is now {self.display_spell_check_status()}.")
            raise StartAgainException
        else:
            print('Back to the main game.')

    def get_save_data(self):
        return self.save_data

    def update_save_data(self, answer, guessed_list, start_time, end_time):
        entry = {'answer': answer, 'guess': guessed_list,
                 'time': [start_time, end_time]}
        self.save_data.append(entry)

    def welcome(self):
        print(f"""   ---------------------------------WELCOME---------------------------------
        Hi {self.name}, welcome to the game! 
        You will have 6 chances to guess a 5-letter word.
        Type '\\q' to exit the app anytime. Type '\\r' to start a new game.
        Type '\\sc' to toggle on and off spell checks. (NOTE: it will restart the game)
    -------------------------------------------------------------------------""")
