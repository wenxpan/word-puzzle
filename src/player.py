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
    """Player profile class.

    A class that stores player attributes, 
    including player name, spell check status, 
    number of chances, selected word list, and 
    game records.

    Methods including getting, setting and toggling 
    these attributes, as well as importing and exporting
    data using json.
    """

    def __init__(self):
        # default values are set when instances are created
        # to prevent save file corruption
        self.name = "default_user"
        self.spell_check_enabled = True
        self.num_chances = 6
        self.list_path = "word_lists/5-letter-words-easy.txt"
        self.records = []

    # player name - getter and setter

    def set_name(self, name):
        self.name = name

    def rename(self):
        # loop until a valid input is received
        while True:
            name = input("Enter new name (15 characters max):\n")
            if len(name) <= 15:
                self.set_name(name)
                print("Renamed successfully! "
                      f"You are now called {self.name}")
                return self.name
            else:
                print("Invalid input. Try again.")

    def get_name(self):
        return self.name

    # spell check status getter, setter and toggler

    def get_spell_check_enabled(self):
        return self.spell_check_enabled

    def display_spell_check_status(self):
        # return spell check status as a string
        return "ON" if self.spell_check_enabled else "OFF"

    def toggle_spell_check_enabled(self):
        # toggle spell check on or off
        self.spell_check_enabled = not self.spell_check_enabled
        print(
            "Spell check setting is now "
            f"{self.display_spell_check_status()}.")

    # number of changes - getter and setter

    def get_num_chances(self):
        return self.num_chances

    def set_num_chances(self):
        # loop and validate if input is a whole number
        while True:
            num = input("Enter number of chances:\n")
            try:
                # if input can be converted to integer, set number
                self.num_chances = int(num)
                print(f"You now have {self.num_chances} attempts.")
                return self.num_chances
            # if input is not integer, go back to loop start
            except ValueError:
                print("Please input whole number. Try again.")

    # word list file path - getter and setter

    def get_list_path(self):
        return self.list_path

    def set_list_path(self):
        # Guides user through selecting word list.

        # display prompt
        print("""       Selecting word list - "
        You can upload custom txt files to the word_lists folder.
        (Note: the file should contain words longer than 2 characters)
        Current options: 
        """)
        # list all the files in the directory
        file_list = os.listdir("word_lists")
        # iterate file list and display file index
        # and name like "0 - filename.txt"
        for i, v in enumerate(file_list):
            print(f"{i} - {v}")
        # loop until user enters valid input to select a word list
        while True:
            try:
                max_index = len(file_list)-1
                # let user input new file index and convert to integer
                new_index = int(
                    input("please enter the file number "
                          f"you want to use (0 to {max_index})\n\n"))
                # if new index is bigger than 0
                # and not exceed max-index, set file path
                if new_index in range(0, len(file_list)):
                    # generate new file path
                    new_path = f"word_lists/{file_list[new_index]}"
                    self.list_path = new_path
                    # print sucess message and remind about spell check
                    print(
                        f"Word list now set to {new_path}\n"
                        "Note: toggle off spell check "
                        "if the words cannot be found in dictionary.")
                    break
                # prevents user from entering negative values
                else:
                    raise ValueError
            # if input is out of range or not an integer,
            # print error message and go back to loop start
            except ValueError:
                print(
                    f"Input invalid. Try again.")

    # file handling methods - saving and loading data using json

    def save_data(self):
        # save keys and values dict to a json file
        save = self.__dict__
        with open(f"user_data/save_data.json", "w") as f:
            json.dump(save, f, indent=4)

    def load_data(self):
        # try accessing values from json file
        try:
            with open(f"user_data/save_data.json") as f:
                save = json.load(f)
                self.name = save["name"]
                self.spell_check_enabled = save["spell_check_enabled"]
                self.num_chances = save["num_chances"]
                self.list_path = save["list_path"]
                self.records = save["records"]
        # if there are entries missing or json file is corrupted,
        # warn the user that default settings will be used
        except KeyError and json.decoder.JSONDecodeError:
            print_red(
                "WARNING: Save file corrupted."
                "Upload backups to replace user_data/save_data.json,"
                "or default settings will be used.")

    def calculate_wins(self):
        # calculate number of wins based on records
        win_count = 0
        for round in self.records:
            if round["answer"] in round["guess"]:
                win_count += 1
        all_count = len(self.records)
        return f"{win_count}/{all_count}"

    def show_status(self):
        # print user profile with relevant information
        print(f"""
        ------------------------PLAYER PROFILE---------------------------
         Player: {self.name}
         Total wins: {self.calculate_wins()}
         Spellcheck: {self.display_spell_check_status()}
         Number of chances for each game: {self.num_chances}
         Selected word list: {self.list_path}
        -----------------------------------------------------------------
        """)

    # records - getter, setter and deleter

    def get_records(self):
        return self.records

    def update_records(self, answer, guessed_list, start_time):
        # add game round to records list
        entry = {"answer": answer, "guess": guessed_list,
                 "start_time": start_time}
        self.records.append(entry)

    def clear_records(self):
        # confirm if user wants to clear records
        confirm_prompt = input("Clearing all records? Type 'Y' to confirm.\n")
        if confirm_prompt.upper() == "Y":
            self.records = []
            print("Records cleared.")
        else:
            print("Back to setting.")

    def export_records(self, record_list, file_name):
        # export records as a user-friendly txt file
        try:
            # check if there are records in the record list
            if record_list:
                with open(f"user_data/record_{file_name}.txt", "w") as f:
                    # loop over record list and write
                    for entry_dict in record_list:
                        # get answer, total guesses and start time
                        answer = entry_dict["answer"]
                        guessed_list = entry_dict["guess"]
                        time = entry_dict["start_time"]
                        # write the first line - start time
                        f.write(f"Start time: {time}\n")
                        # write a decorating line
                        # (length will change based on word length)
                        decorating_line = f"{'=' * (2*len(answer) + 7)}\n"
                        f.write(decorating_line)
                        # write each word in one line
                        for word in guessed_list:
                            f.write(f"  | {' '.join(word)} |  \n")
                        f.write(decorating_line)
                        # write correct word
                        f.write(f"CORRECT WORD IS: {answer}\n\n")
                    # after writing, show success message
                    print(
                        "Record exported! You can find it in "
                        f"user_data/record_{file_name}.txt")
            # If no records found, show message
            else:
                print("no record found.")
        # if not able to write file, show error message
        except IndexError:
            print(
                f"Save data corrupted."
                "Clear all records to export future games.")

    def export_records_all(self):
        # export all records of a player
        self.export_records(self.records, self.name)

    def export_records_latest(self):
        # export record of current game play
        # extract current record from all the records
        latest_record = self.records[-1]
        # use start time of the record as file name
        start_time = latest_record["start_time"]
        # use helper function to convert time in a different format
        start_time_formatted = convert_time_string(
            start_time, "%Y-%m-%d %H:%M:%S", "%Y%m%d%H%M%S")
        self.export_records([latest_record], start_time_formatted)
