from player import create_player
from rich.prompt import Prompt
from rich import print


def show_options():
    message = """               Settings:
                [bold]1 - rename
                2 - toggle spell check
                3 - change word list
                4 - set number of chances
                5 - export all records as txt file
                6 - clear records[/bold]
                help - show options
                show - show current profile
                save - save changes
                reset - discard changes
                quit - quit
    """
    print(message)


def change_settings_loop(player):
    while True:
        prompt = input(
            "\n**What do you want to do? (Enter 'help' for a list of options)**\n")
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
            case "help":
                show_options()
            case "show":
                player.show_status()
            case "save":
                player.save_data()
                print("**Changes saved.**\n")
            case "reset":
                player.load_data()
                print("\n**Changes discarded. Status loaded from last saved.**\n")
                player.show_status()
            case "quit":
                confirm = input(
                    "\n**Confirm you want to quit? Type 'Y' to confirm.**\n").upper()
                if confirm == "Y":
                    break
            case other:
                print("**Invalid input. Try again.**")


def setting():
    player = create_player()
    print(f"\n        Welcome, {player.get_name()}!")
    player.show_status()
    show_options()
    change_settings_loop(player)
    print("See you next time!")


if __name__ == "__main__":
    setting()
