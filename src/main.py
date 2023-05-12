from guess import play_loop
from player_setting import setting
from sys import argv

if __name__ == "__main__":
    if argv[1] == "play":
        play_loop()
    elif argv[1] == "settings":
        setting()
    else:
        print("Something went wrong. Please try reopening.")
