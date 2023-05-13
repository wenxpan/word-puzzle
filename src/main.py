import guess
import player_setting
from sys import argv

if __name__ == "__main__":
    try:
        if argv[1] == "play":
            guess.play_loop()
        elif argv[1] == "settings":
            player_setting.setting()
        else:
            print("Invalid command. "
                  "Please enter 'play' or 'settings' and retry.")
    # catching error when user open py file directly
    except IndexError:
        print("Not enough arguments. "
              "Please follow the help doc and try again.")
