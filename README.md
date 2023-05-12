# WenxuanPan_T1A3

## Links (R2)

- [Github repo](https://github.com/wenxuan-pan/WenxuanPan_T1A3)

## References (R3)

- [rich - Pypi](https://pypi.org/project/rich/) - I used this python library to render colored and styled text.
- [pyspellchecker - Pypi](https://pypi.org/project/pyspellchecker/) - I used this python library to check spelling of user input.
- I referred to the following text files to generate word lists:
  - [The Stanford GraphBase: A Platform for Combinatorial Computing](https://www-cs-faculty.stanford.edu/~knuth/sgb.html): I used this to generate two lists with 5-letter words.
  - [common-7-letter-words - Github](https://github.com/powerlanguage/word-lists/blob/master/common-7-letter-words.txt)
  - [google-profanity-words - Github](https://github.com/coffee-and-fun/google-profanity-words): I used this list to filter out inappropriate words in the 5-letter-word list
  - [Wordle - New York Times](https://www.nytimes.com/games/wordle/index.html): This project takes inspiration and extends from the popular word game Wordle.
  - [A Python Wordle Clone - Practice Python](https://www.practicepython.org/blog/2022/02/12/wordle.html): I referred to the codes in this webpage to develop my function to compare two words
  - [Text to ASCII Art Generator - patorjk](http://patorjk.com/software/taag/): I used this link to generate the ascii art for my title

## Style guide (R5)

Identify any code style guide or styling conventions that the application will adhere to.

## Features (R6)

Word Pie consists of the following features:

### Draw a random word from a given word list

- The program will read the txt file in the given directory and generate a word list; it will then select a random word for user to guess.
- Error handling is integrated to deal with cases when the text file is empty or contains no word more than 2 characters.
- The random word is stored in a variable to allow for further uses.

### Takes user input and check if it follows game's rule

- The program reveals the number of letters for the word and asks the user to take a guess. It then compares the guessed with the answer.
- It validates that the guess is an English word and/or contains alphabetic letters only. Loops and conditional structures are utilised to repeatedly ask for user input until a valid response is received.

#### Allow user to restart and quit the game at any time

- This can be considered as the sub-feature for taking user input. Conditionals and error handling is utlisied, so that when the user types special commands, exception will be raised and then catched outside the loop to restart/quit the game gracefully.

### Compare user's guess with answer and display differences

- The program checks the guess to see if it matches the answer. Two functions are used - one is to check if the guess equals to answer, and is used as a condition in the if/else statement. The other function is to analyse and display which letters are correct (in the answer word and in the same place), misplaced or wrong (not in the word).
- External package Rich is used to highlight letters in different colours.

### Display progress information throughout the gameplay

- The user has a certain number of attempts to guess the word. Loops are used to repeatedly get input until the user runs out of chances. Guessing the correct word early will also break the loop.
- During each round, relevant information will be displayed including the user's previous guesses, number of chances used and total chances, spell check status (whether the program will check if the user's guess is an English word), as well as some narrative text.

### Show ending message based on result

- The game will display different ending message when user fails/succeeds in guessing the word.
- Random package is used so that the message text will not be the same everytime.

### Export records as text file

- The user will be able to export formatted records as txt files and the program will display the exported file path.
- They have the option to export records of one round each time game ends, where the save file will be named after the start time of the session; or they can go to settings and export all the records into one file, with file name being their profile name.

### Customise player profile and settings

- The player can access settings and have a number of customise options, including renaming, selecting the word list, toggling spell check status, setting the number of chances, exporting records as txt file and clearing all records. The player profile will also be displayed each time they open settings.
- Player class is created to encapsulate all the relevant information of the user. When instance of the class is created, methods such as getters and setters are imported and can be used in both main play and settings mode.
- bash scripts are used to pass on arguments to the python file, and with the help of conditional structures, the player can easily switch between 'play' and 'settings' mode.

### Save and load data using json

- Player's information will be exported to a json file and imported back to the object when the program reopens.
- Error handling is utlitised to deal with missing or corrupted files - when it catches relevant exceptions, default information will be set to allow the program to continue.

## Implementation Plan (R7)

## Help Documentation (R8)
