import json


class StartAgainException(Exception):
    pass


# class with game settings
class Player():
    def __init__(self, name):
        self.spell_check_enabled = True
        self.name = name
        self.records = []

    def save_data(self):
        save = {"name": self.name,
                "spell_check_enabled": self.spell_check_enabled, "records": self.records}
        with open(f'user_data/save_{self.name}.json', 'w') as f:
            json.dump(save, f, indent=4)
        print(f'data saved to user_data/save_{self.name}.json')

    def load_data(self):
        try:
            with open(f'user_data/save_{self.name}.json') as f:
                save = json.load(f)
                self.spell_check_enabled = save["spell_check_enabled"]
                self.records = save["records"]
            print(
                f'data loaded from user_data/save_{self.name}.json\ndata: {save}')
        except FileNotFoundError:
            pass

    def welcome(self):
        print(f"""   ---------------------------------WELCOME---------------------------------
        Hi {self.name}, welcome to the game! 
        You will have 6 chances to guess a 5-letter word.
        Type '\\q' to exit the app anytime. Type '\\r' to start a new game.
        Type '\\sc' to toggle on and off spell checks. (NOTE: it will restart the game)
    -------------------------------------------------------------------------""")

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

    def get_records(self):
        return self.records

    def update_records(self, answer, guessed_list, start_time, end_time):
        entry = {'answer': answer, 'guess': guessed_list,
                 'time': [start_time, end_time]}
        self.records.append(entry)
