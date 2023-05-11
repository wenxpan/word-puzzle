from rich import print


def print_welcome(name, num_chances):
    welcome_message = f"""
   _       ______  ____  ____     ____  __________
  | |     / / __ \/ __ \/ __ \   / __ \/  _/ ____/
  | | /| / / / / / /_/ / / / /  / /_/ // // __/   
  | |/ |/ / /_/ / _, _/ /_/ /  / ____// // /___   
  |__/|__/\____/_/ |_/_____/  /_/   /___/_____/   

  Hello, {name}! Welcome to WORD PIE.

  Mr. Python is hungry, and all he wants is that delicious but poisonous pie.
  He has to cast the correct spell to consume it safely!
  Can you help him find the secret word in {num_chances} attempts? 
  A Friendly Fairy agrees to reveal hints as you go along:
    - [bold black on bright_green]Green[/bold black on bright_green] means the letter is in the secret word and at the same place.
    - [bold black on bright_yellow]Yellow[/bold black on bright_yellow] means the letter is in the secret word but at the wrong place.
    - [bold black on white]Grey[/bold black on white] means the letter is not in the secret word.
  """
    print(welcome_message)


# print_welcome('user', 10)


hint_message = [
    "Mr. Python stares at the pie eagerly.",
    "Mr. Python stares at you. You feel cold sweat.",
    "Mr. Python's tongues flicks.",
    "Friendly Fairy reveals a hint",
    "Mr. Python thanks the Friendly Fairy.",
    "Friendly Fairy looks at you encouragingly.",
    "The pie just moved an inch; or maybe just an illusion..."
    "The pie is turning purple somehow."
]

win_message = [
    "Yum Yum! Mr. Python is really happy.",
    "You feel relieved.",
    "Mr. Python invites you to join the feast."
]


lose_message = [
    "Mr. Python couldn't wait! He inhaled the pie and lost 500 health points.",
    "Too late! Poisonous Pie dissolved on the ground.",
    "Friendly Fairy shrugged and flew away.",
    "A portal opened and the pie vanished. The pie is a lie!",
    "Poisonous Pie got impatient and walked away."
]
