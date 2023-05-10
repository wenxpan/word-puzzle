from player import validate_player
import os


def show_options():
    instructions = {
        '1': 'toggle spell check',
        '2': 'show records',
        '3': 'export records (txt)',
        '4': 'select word list',
        '5': 'save changes',
        '6': 'close'}
    message = 'What do you want to do?\n'
    for k, v in instructions:
        message += f'{k} - {v}\n'
    return message


def setting():
    player = validate_player()
    print(f'Welcome, {player.name}!')  # change this to method
    player.show_status()
    while True:
        prompt = input(show_options())
        if prompt == "1":
            player.toggle_spell_check_enabled()
        elif prompt == "2":
            pass
        elif prompt == "3":
            pass
        elif prompt == "4":
            pass
        elif prompt == "5":
            player.save_data()
            print('Changes saved.')
            break
        elif prompt == "6":
            confirm = input(
                'Discarding all changes and quit? Type "Y" to confirm.').upper()
            if confirm == "Y":
                break
        else:
            print('Invalid input.')
    print('See you next time!')


if __name__ == '__main__':
    setting()
