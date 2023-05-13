from player import create_player
from rich import print


def show_options():
    """print a list of commands available for user"""
    message = """           Commands (case-insensitive):
            [bold]1 - rename
            2 - toggle spell check
            3 - change word list
            4 - set number of chances
            5 - export all records as txt file
            6 - clear records[/bold]
            help - show commands
            show - show current profile
            quit - quit
    """
    print(message)


def change_settings_loop(player):
    """Repeatedly ask user to input commands 
    until they choose to close settings
    """
    while True:
        # convert command to uppercase
        prompt = input(
            "\n**What do you want to do? (Enter 'help' for a "
            "list of commands)**\n").upper()
        match prompt:
            case "1":
                player.rename()
            case "2":
                player.toggle_spell_check_enabled()
            case "3":
                player.set_list_path()
            case "4":
                player.set_num_chances()
            case "5":
                player.export_records_all()
            case "6":
                player.clear_records()
            case "HELP":
                show_options()
            case "SHOW":
                player.show_status()
            case "QUIT":
                # ask if the changes are to be saved
                will_save = input(
                    "\n**Save changes before quit?\n"
                    "Type 'Y' to save, type any other buttons "
                    "to discard all changes.**\n")
                if will_save.upper() == "Y":
                    player.save_data()
                    print("**Changes saved.**\n")
                else:
                    print("Changes discarded.")
                # end the loop
                break
            # consider any other input to be invalid
            case other:
                print("**Invalid input. Try again.**")


def setting():
    """main settings"""
    # create a player object
    player = create_player()
    # get and display player name
    name = player.get_name()
    print(f"\n        Welcome, {name}!")
    # show player profile
    player.show_status()
    # show a list of commands
    show_options()
    # ask for user input
    change_settings_loop(player)
    # when loop ends, display quit message
    print(f"See you next time, {name}!")
