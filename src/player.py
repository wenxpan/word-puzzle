import json
import os
from helper import print_red, convert_time_string


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


class Player():
    """ Player profile class.

    A class that stores player attributes, 
    including player name, spell check status, 
    number of chances, selected word list, and 
    game records.

    Methods including getting, setting and toggling 
    these attributes, as well as importing and exporting
    data using json.
    """

    def __init__(self):
        self.name = "default_user"
        self.spell_check_enabled = True
        self.num_chances = 6
        self.list_path = "word_lists/5-letter-words-easy.txt"
        self.records = []

    # name getter, setter and rename methods
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

    # spell check status getter, setter and toggler
    def get_spell_check_enabled(self):
        return self.spell_check_enabled

    def display_spell_check_status(self):
        """return spell check status as string"""
        return "ON" if self.spell_check_enabled else "OFF"

    def toggle_spell_check_enabled(self):
        """toggle spell check on or off"""
        self.spell_check_enabled = not self.spell_check_enabled
        print(
            f"Spell check setting is now {self.display_spell_check_status()}.")

    # number of changes - getter and setter
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

    # word list file path - getter and setter
    def get_list_path(self):
        return self.list_path

    def set_list_path(self):
        """Guides user through selecting word list."""

        # display prompt
        print("""       Selecting word list - "
        You can upload custom word lists to the word_lists folder.
        (Note: the list should be txt file and contain words longer than 2 characters)
        Current options: 
        """)
        # list all the files in the directory
        file_list = os.listdir("word_lists")
        # iterate file list and display file index and name like "0 - filename.txt"
        for i, v in enumerate(file_list):
            print(f"{i} - {v}")
        # loop until user enters valid input to select a word list
        while True:
            try:
                max_index = len(file_list)-1
                # let user input new file index
                new_index = int(
                    input(f"please enter the file number you want to use (0 to {max_index})\n\n"))
                # if new index is bigger than 0 and not exceed max-index, set file path
                if new_index in range(0, len(file_list)):
                    new_path = f"word_lists/{file_list[new_index]}"
                    self.list_path = new_path
                    # print sucess message and remind about spell check
                    print(
                        f"Word list now set to {new_path}\n"
                        "Note: toggle off spell check if the words cannot be found in dictionary.")
                    break
                else:
                    raise ValueError
            # if the input raises error, print error message and go back to loop start
            except ValueError:
                print(
                    f"Input invalid. Try again.")

    def save_data(self):
        save = {"name": self.name,
                "spell_check_enabled": self.spell_check_enabled,
                "num_chances": self.num_chances,
                "list_path": self.list_path,
                "records": self.records}
        with open(f"user_data/save_data.json", "w") as f:
            json.dump(save, f, indent=4)

    def load_data(self):
        try:
            with open(f"user_data/save_data.json") as f:
                save = json.load(f)
                self.name = save["name"]
                self.spell_check_enabled = save["spell_check_enabled"]
                self.num_chances = save["num_chances"]
                self.list_path = save["list_path"]
                self.records = save["records"]
            print("*data loaded from user_data/save_data.json*")
        except KeyError and json.decoder.JSONDecodeError:
            print_red(
                "WARNING: Save file corrupted. Upload backup save to replace user_data/save_data.json, or default settings will be used.")

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

    def get_records(self):
        return self.records

    def update_records(self, answer, guessed_list, start_time):
        entry = {"answer": answer, "guess": guessed_list,
                 "start_time": start_time}
        self.records.append(entry)

    def clear_records(self):
        if input("Clearing all records? Type 'Y' to confirm.\n").upper() == "Y":
            self.records = []
            print("All cleared!")
        else:
            print("Back to setting.")

    # export record as txt file
    def export_records(self, record_list, file_name):
        try:
            if record_list:
                with open(f"user_data/record_{file_name}.txt", "w") as f:
                    for entry_dict in record_list:
                        answer = entry_dict["answer"]
                        guessed_list = entry_dict["guess"]
                        time = entry_dict["start_time"]

                        f.write(f"Start time: {time}\n")
                        decorating_line = f"{'=' * (2*len(answer) + 7)}\n"
                        f.write(decorating_line)
                        for word in guessed_list:
                            f.write(f"  | {' '.join(word)} |  \n")
                        f.write(decorating_line)
                        f.write(f"CORRECT WORD IS: {answer}\n\n")
                    print(
                        f"Record exported! You can find it in user_data/record/record_{file_name}.txt")
            else:
                print("no record found.")
        except IndexError:
            print(
                f"Save data corrupted. Please do not edit the save file.\nClear all records to export future games.")

    def export_records_all(self):
        self.export_records(self.records, self.name)

    def export_records_latest(self):
        latest_record = self.records[-1]
        start_time = latest_record["start_time"]
        start_time_formatted = convert_time_string(
            start_time, "%Y-%m-%d %H:%M:%S", "%Y%m%d%H%M%S")
        self.export_records(latest_record, start_time_formatted)
