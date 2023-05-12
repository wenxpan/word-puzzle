from rich import print
import random


def print_welcome(name, num_chances):
    welcome_message = (
        f"""   _       ______  ____  ____     ____  __________
  | |     / / __ \/ __ \/ __ \   / __ \/  _/ ____/
  | | /| / / / / / /_/ / / / /  / /_/ // // __/   
  | |/ |/ / /_/ / _, _/ /_/ /  / ____// // /___   
  |__/|__/\____/_/ |_/_____/  /_/   /___/_____/   

  Hello, {name}! Welcome to [bold]WORD PIE[/bold], a word guessing game.

  [bold]Mr. Python[/bold] is hungry, and all he wants is that delicious but [bold]Poisonous Pie[/bold].
  He has to cast the correct healing spell to swallow it safely!
  Can you help him find the secret word in {num_chances} attempts? 
  [bold]Friendly Fairy[/bold] agrees to reveal hints as you go along:
    - [bold black on bright_green]Green[/bold black on bright_green] means the letter is in the secret word and at the same place.
    - [bold black on bright_yellow]Yellow[/bold black on bright_yellow] means the letter is in the secret word but at the wrong place.
    - [bold black on white]Grey[/bold black on white] means the letter is not in the secret word.
  """)
    print(welcome_message)


hint_messages = [
    "Mr. Python stares at the Poisonous Pie eagerly.",
    "Mr. Python stares at you. You feel cold sweat.",
    "Mr. Python's tongues flicks.",
    "Friendly Fairy reveals a hint.",
    "Mr. Python thanks the Friendly Fairy.",
    "Friendly Fairy looks at you encouragingly.",
    "Poisonous Pie just moved an inch; maybe an illusion...",
    "Poisonous Pie is starting to turn [purple]purple[/purple].",
    "Poisonous Pie smells putrid.",
    "Mr. Python comes closer to the Poisonous Pie."
]

win_messages = [
    "Yum yum. Mr. Python was really happy.",
    "You felt relieved.",
    "Mr. Python invited you to join the feast.",
    "Mr. Python tossed a small piece of the pie to Friendly Fairy.",
    "Friendly Fairy smiled and flew away."
]

lose_messages = [
    "Mr. Python couldn't wait! He inhaled the pie and lost 500 health points.",
    "Too late! Poisonous Pie dissolved on the ground.",
    "Friendly Fairy shrugged and flew away.",
    "A portal opened and Poisonous Pie vanished. The pie is a lie!",
    "Poisonous Pie got impatient and walked away.",
    "Mr. Python swallowed the pie, then turned to look at you."
]
