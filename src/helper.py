from rich import print
from datetime import datetime


def print_red(text):
    print(f"[red bold]{text}[/red bold]")


class StartAgainException(Exception):
    pass


def current_time_string(format):
    time = datetime.now().strftime(format)
    return time


def convert_time_string(time, old_format, new_format):
    time_object = datetime.strptime(time, old_format)
    new_time = time_object.strftime(new_format)
    return new_time


def highlight_text(text, fore, bg):
    return f"[{fore} on {bg}]{text}[/{fore} on {bg}]"
