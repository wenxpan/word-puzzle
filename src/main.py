from guess import play_loop
from player_setting import setting
from sys import argv

if __name__ == "__main__":
    try:
        if argv[1] == "play":
            play_loop()
        elif argv[1] == "settings":
            setting()
        else:
            print("Invalid command. "
                  "Please enter 'play' or 'settings' and retry.")
    # catching error when user open py file directly
    except IndexError:
        print("Not enough arguments. "
              "Please follow the help doc and try again.")
