from player import create_player
from rich.prompt import Prompt
from rich import print


def show_options():
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
    while True:
        prompt = input(
            "\n**What do you want to do? (Enter 'help' for a list of commands)**\n").upper()
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
                will_save = input(
                    "\n**Save changes before quit?\n"
                    "Type 'Y' to save, type any other buttons to discard all changes.**\n")
                if will_save.upper() == "Y":
                    player.save_data()
                    print("**Changes saved.**\n")
                else:
                    print("Changes discarded.")
                break
            case other:
                print("**Invalid input. Try again.**")


def setting():
    player = create_player()
    name = player.get_name()
    print(f"\n        Welcome, {name}!")
    player.show_status()
    show_options()
    change_settings_loop(player)
    print(f"See you next time, {name}!")


if __name__ == "__main__":
    setting()
