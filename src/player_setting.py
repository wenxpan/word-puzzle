from player import validate_player
import os


def show_options():
    instructions = {
        '1': 'toggle spell check',
        '2': 'show records',
        '3': 'export records (txt)',
        '4': 'select word list',
        '5': "rename",
        '\\s': 'save changes',
        '\\r': 'reset',
        '\\q': 'close'}
    message = 'What do you want to do?\n'
    for k, v in instructions.items():
        message += f'{k} - {v}\n'
    return message


def setting():
    player = validate_player()
    print(f'Welcome, {player.name}!')  # change this to method
    while True:
        player.show_status()
        prompt = input(show_options())
        match prompt:
            case "1":
                player.toggle_spell_check_enabled()
            case "2":
                pass
            case "3":
                pass
            case "4":
                player.set_list_path()
            case "\\s":
                player.save_data()
                print('Changes saved.\n')
            case '\\r':
                player.load_data()
                pass
            case "\\q":
                confirm = input(
                    'Confirm you want to quit? Type "Y" to confirm.\n').upper()
                if confirm == "Y":
                    break
            case other:
                print('Invalid input.')
    print('See you next time!')


if __name__ == '__main__':
    setting()
