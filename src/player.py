import json
import os


class StartAgainException(Exception):
    pass


def validate_player():
    try:
        player = Player()
        player.load_data()
    except FileNotFoundError:
        prompt = input(
            'Enter your name to create a profile:\n')
        player = Player()
        player.set_name(prompt)
        player.save_data()
    return player


# class with game settings
class Player():
    def __init__(self):
        self.spell_check_enabled = True
        self.name = ''
        self.records = []
        self.list_path = 'word_lists/5-letter-words-easy.txt'

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_list_path(self):
        return self.list_path

    def set_list_path(self, path):
        print('Current lists in the folder:')
        print(os.listdir('word_lists'), sep='\n')
        path = input('please enter the file name you want to use')
        self.list_path = f'word_lists/{path}'

    def save_data(self):
        save = {"name": self.name,
                "spell_check_enabled": self.spell_check_enabled, "records": self.records}
        with open(f'user_data/save_data.json', 'w') as f:
            json.dump(save, f, indent=4)
        print(f'data saved to user_data/save_data.json')

    def load_data(self):
        with open(f'user_data/save_data.json') as f:
            save = json.load(f)
            self.name = save["name"]
            self.spell_check_enabled = save["spell_check_enabled"]
            self.records = save["records"]
        print(
            f'data loaded from user_data/save_data.json')

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
        print(f'Selected word list: {self.list_path}')

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
