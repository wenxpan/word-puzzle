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
        self.name = 'user'
        self.records = []
        self.list_path = 'word_lists/5-letter-words-easy.txt'
        self.num_chances = 6

    def get_num_chances(self):
        return self.num_chances

    def set_num_chances(self):
        num = input('Enter number of chances:\n')
        while True:
            try:
                self.num_chances = int(num)
                break
            except:
                print('Please input number. Try again.')

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_list_path(self):
        return self.list_path

    def set_list_path(self):
        print('Current lists in the folder:')
        path_list = os.listdir('word_lists')
        for i, v in enumerate(path_list):
            print(f'{i+1} - {v}')
        while True:
            try:
                path_index = int(
                    input('please enter the file name you want to use\n\n')) - 1
                x = range(1, len(path_list))
                print('index', x)
                if path_index in range(0, len(path_list)):
                    self.list_path = f'word_lists/{path_list[path_index]}'
                    print(
                        f'word list now set to word_lists/{path_list[path_index]}')
                    break
                else:
                    raise ValueError
            except ValueError:
                print('invalid. try again.')

    def save_data(self):
        save = {"name": self.name,
                "spell_check_enabled": self.spell_check_enabled,
                "num_chances": self.num_chances,
                "list_path": self.list_path,
                "records": self.records}
        with open(f'user_data/save_data.json', 'w') as f:
            json.dump(save, f, indent=4)
        print(f'data saved to user_data/save_data.json')

    def load_data(self):
        with open(f'user_data/save_data.json') as f:
            save = json.load(f)
            try:
                self.name = save["name"]
                self.spell_check_enabled = save["spell_check_enabled"]
                self.num_chances = save["num_chances"]
                self.list_path = save["list_path"]
                self.records = save["records"]
            except:
                print(
                    'save file corrupted. Default settings will be used.')
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
        print(f'Player: {self.name}')
        print(f'spellcheck: {self.display_spell_check_status()}')
        print(f'number of chances:{self.num_chances}')
        print(f'Selected word list: {self.list_path}')

    def welcome(self):
        print(f"""   ---------------------------------WELCOME---------------------------------
        Hi {self.name}, welcome to the game! 
        You will have {self.num_chances} chances to guess a English word.
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

    # export record as txt file

    def export_record(self, guessed_list, answer, name):
        with open(f'user_data/record_{name}.txt', 'w') as f:
            decorator = f'{"=" * (2*len(answer) + 7)}\n'
            f.write(decorator)
            for word in guessed_list:
                f.write(f"  | {' '.join(word)} |  \n")
            f.write(decorator)
            f.write(f'CORRECT WORD IS: {answer}\n')
        print(
            f"Record saved! You can find it in user_data/record/record_{name}.txt")

    def export_all_records(self):
        record_list = self.records
        with open(f'user_data/record_{self.name}.txt', 'w') as f:
            for entry_dict in record_list:
                answer = entry_dict['answer']
                guessed_list = entry_dict['guess']
                time = entry_dict['time'][0]

                f.write(f'Start time: {time}\n')
                decorator = f'{"=" * (2*len(answer) + 7)}\n'
                f.write(decorator)
                for word in guessed_list:
                    f.write(f"  | {' '.join(word)} |  \n")
                f.write(decorator)
                f.write(f'CORRECT WORD IS: {answer}\n\n')


# "records": [
#         {
#             "answer": "STONE",
#             "guess": [
#                 "APPLE",
#                 "APPLY"
#             ],
#             "time": [
#                 "2023-05-11 13:15:43",
#                 "2023-05-11 13:16:05"
#             ]
#         },
#         {
#             "answer": "CRIPPLE",
#             "guess": [
#                 "CRIPPLE"
#             ],
#             "time": [
#                 "2023-05-11 13:54:10",
#                 "2023-05-11 13:54:14"
#             ]
#         }]
