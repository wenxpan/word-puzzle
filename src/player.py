import json


class StartAgainException(Exception):
    pass


def validate_player():
    while True:
        name = input('please enter player name.\n')
        try:
            with open(f'user_data/save_{name}.json') as f:
                player = Player(name)
                player.load_data()
                return player
        except FileNotFoundError:
            prompt = input(
                'profile not found. Enter "Y" to create a profile. Enter any other key to enter another player name.\n')
            if prompt == "Y":
                player = Player(name)
                player.save_data()
                return player


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
        with open(f'user_data/save_{self.name}.json') as f:
            save = json.load(f)
            self.spell_check_enabled = save["spell_check_enabled"]
            self.records = save["records"]
        print(
            f'data loaded from user_data/save_{self.name}.json')

    def calculate_wins(self):
        win_count = 0
        for round in self.records:
            if round["answer"] in round["guess"]:
                win_count += 1
        all_count = len(self.records)
        return f'Total wins: {win_count}/{all_count}'

    def show_status(self):
        print(self.calculate_wins())
        print(f'spellcheck: {self.display_spell_check_status()}')
        print('options: toggle Spellcheck / upload word list / export records')

    def welcome(self):
        print(f"""   ---------------------------------WELCOME---------------------------------
        Hi {self.name}, welcome to the game! 
        You will have 6 chances to guess a 5-letter word.
        Type '\\q' to exit the app anytime. Type '\\r' to restart the game.
    -------------------------------------------------------------------------""")

    # get current spell check state
    def get_spell_check_enabled(self):
        return self.spell_check_enabled

    def display_spell_check_status(self):
        return 'ON' if self.spell_check_enabled else 'OFF'

    # toggle spell check on or off
    def toggle_spell_check_enabled(self):
        self.spell_check_enabled = not self.spell_check_enabled
        print(
            f"Spell check setting is now {self.display_spell_check_status()}.")

    def get_records(self):
        return self.records

    def update_records(self, answer, guessed_list, start_time, end_time):
        entry = {'answer': answer, 'guess': guessed_list,
                 'time': [start_time, end_time]}
        self.records.append(entry)

    def delete_player(self):
        pass

    def clear_record(self):
        self.records = []

    def display_records(self):
        pass

    def export_records(self):
        pass

    # export record as txt file
    def export_record(self, guessed_list, answer, name):
        with open(f'user_data/record_{name}.txt', 'w') as f:
            f.write('=================\n')
            for word in guessed_list:
                f.write(f"  | {' '.join(word)} |  \n")
            f.write('=================\n')
            f.write(f'CORRECT WORD IS: {answer}\n')
        print(
            f"Record saved! You can find it in user_data/record/record_{name}.txt")
