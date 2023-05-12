from player import create_player


def show_options():
    message = """
    1 - toggle spell check
    2 - export records (txt)
    3 - select word list
    4 - rename
    5 - set number of chances
    6 - clear records
    \\h - show options
    \\s - save changes
    \\r - discard changes
    \\q - quit
    """
    print(message)


def change_settings_loop(player):
    show_options()
    while True:
        player.show_status()
        prompt = input(
            "What do you want to do?\nEnter \\h to show a list of options available")
        match prompt:
            case "1":
                player.toggle_spell_check_enabled()
            case "2":
                player.export_records_all()
            case "3":
                player.set_list_path()
            case "4":
                player.set_name(input("Enter new name:\n"))
            case "5":
                player.set_num_chances()
            case "6":
                player.clear_records()
            case "\\h":
                show_options()
            case "\\s":
                player.save_data()
                print('Changes saved.\n')
            case '\\r':
                player.load_data()
            case "\\q":
                confirm = input(
                    'Confirm you want to quit? Type "Y" to confirm.\n').upper()
                if confirm == "Y":
                    break
            case other:
                print('Invalid input.')


def setting():
    player = create_player()
    print(f'Welcome, {player.get_name()}!')
    change_settings_loop(player)
    print('See you next time!')


if __name__ == '__main__':
    setting()
