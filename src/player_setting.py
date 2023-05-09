from player import validate_player


def setting():
    player = validate_player()
    print(f'Welcome, {player.name}!')
    player.show_status()
    while True:
        prompt = input(
            '\nWhat do you want to do?\n1 - toggle spell check\n2 - show records\n3 - export records\n4 - Save and close\n5 - Close without save\n')
        if prompt == "1":
            player.toggle_spell_check_enabled()
        elif prompt == "2":
            pass
        elif prompt == "3":
            pass
        elif prompt == "4":
            player.save_data()
            print('Changes saved.')
            break
        elif prompt == "5":
            confirm = input(
                'Discarding all changes and quit? Type "Y" to confirm.')
            if confirm == "Y":
                break
    print('See you next time!')


if __name__ == '__main__':
    setting()
