import json
import os
from datetime import datetime


def create_player():
    try:
        player = Player()
        player.load_data()
    except FileNotFoundError:
        prompt = input(
            "Enter your name to create a profile:\n")
        player = Player()
        player.set_name(prompt)
        player.save_data()
    return player


# class with game settings
class Player():
    def __init__(self):
        self.spell_check_enabled = True
        self.name = "default_name"
        self.records = []
        self.list_path = "word_lists/5-letter-words-easy.txt"
        self.num_chances = 6

    def get_num_chances(self):
        return self.num_chances

    def set_num_chances(self):
        num = input("Enter number of chances:\n")
        while True:
            try:
                self.num_chances = int(num)
                break
            except:
                print("Please input number. Try again.")

    def set_name(self, name):
        self.name = name

    def rename(self):
        while True:
            name = input("Enter new name (15 characters max):\n")
            if len(name) <= 15:
                self.set_name(name)
                print(f"Renamed successfully! You are now called {self.name}")
                break
            else:
                print("Invalid input. Try again.")

    def get_name(self):
        return self.name

    def get_list_path(self):
        return self.list_path

    def set_list_path(self):
        print(
            "\nChanging to another word list - current files in the word_lists folder:")
        file_list = os.listdir("word_lists")
        for i, v in enumerate(file_list):
            print(f"{i} - {v}")
        while True:
            try:
                new_index = int(
                    input("please enter the file index you want to use\n\n"))
                if new_index in range(0, len(file_list)):
                    new_path = f"word_lists/{file_list[new_index]}"
                    self.list_path = {new_path}
                    print(
                        f"Word list now set to {new_path}\nNote: toggle off spell check if the words cannot be found in dictionary.")
                    break
                else:
                    raise ValueError
            except ValueError:
                print("invalid. try again.")

    def save_data(self):
        save = {"name": self.name,
                "spell_check_enabled": self.spell_check_enabled,
                "num_chances": self.num_chances,
                "list_path": self.list_path,
                "records": self.records}
        with open(f"user_data/save_data.json", "w") as f:
            json.dump(save, f, indent=4)
        print(f"data saved to user_data/save_data.json")

    def load_data(self):
        try:
            with open(f"user_data/save_data.json") as f:
                save = json.load(f)
                # for k, _ in save.items():
                # self[k] = save[k]
                self.name = save["name"]
                self.spell_check_enabled = save["spell_check_enabled"]
                self.num_chances = save["num_chances"]
                self.list_path = save["list_path"]
                self.records = save["records"]
            print("*data loaded from user_data/save_data.json*")
        except KeyError:
            print(
                "save file corrupted. Default settings will be used.")

    def calculate_wins(self):
        win_count = 0
        for round in self.records:
            if round["answer"] in round["guess"]:
                win_count += 1
        all_count = len(self.records)
        return f"{win_count}/{all_count}"

    def show_status(self):
        print(f"""
        ------------------------PLAYER PROFILE---------------------------
        Player: {self.name}
        Total wins: {self.calculate_wins()}
        Spellcheck: {self.display_spell_check_status()}
        Number of chances for each game: {self.num_chances}
        Selected word list: {self.list_path}
        -----------------------------------------------------------------
        """)

    # get current spell check state
    def get_spell_check_enabled(self):
        return self.spell_check_enabled

    def display_spell_check_status(self):
        return "ON" if self.spell_check_enabled else "OFF"

    # toggle spell check on or off
    def toggle_spell_check_enabled(self):
        self.spell_check_enabled = not self.spell_check_enabled
        print(
            f"Spell check setting is now {self.display_spell_check_status()}.")

    def get_records(self):
        return self.records

    def update_records(self, answer, guessed_list, start_time, end_time):
        entry = {"answer": answer, "guess": guessed_list,
                 "time": [start_time, end_time]}
        self.records.append(entry)

    def clear_records(self):
        if input("Clearing all records? Type "Y" to confirm.\n").upper() == "Y":
            self.records = []
        else:
            print("Back to setting.")

    # export record as txt file
    def export_records(self, record_list, name):
        if record_list:
            with open(f"user_data/record_{name}.txt", "w") as f:
                for entry_dict in record_list:
                    answer = entry_dict["answer"]
                    guessed_list = entry_dict["guess"]
                    time = entry_dict["time"][0]

                    f.write(f"Start time: {time}\n")
                    decorating_line = f"{'=' * (2*len(answer) + 7)}\n"
                    f.write(decorating_line)
                    for word in guessed_list:
                        f.write(f"  | {' '.join(word)} |  \n")
                    f.write(decorating_line)
                    f.write(f"CORRECT WORD IS: {answer}\n\n")
                print(
                    f"Record exported! You can find it in user_data/record/record_{name}.txt")
        else:
            print("no record found.")

    def export_records_all(self):
        self.export_records(self.records, self.name)

    def export_records_latest(self):
        start_time = self.records[-1]["time"][0]
        start_time_obj = datetime.strptime(
            start_time, "%Y-%m-%d %H:%M:%S")
        start_time_formatted = start_time_obj.strftime("%Y%m%d%H%M%S")
        self.export_records([self.records[-1]], start_time_formatted)
