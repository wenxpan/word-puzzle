from rich import print
from datetime import datetime


def print_red(text):
    """print text in red bold format using rich markup"""
    print(f"[red bold]{text}[/red bold]")


class StartAgainException(Exception):
    """custom exception class for restart"""
    pass


def current_time_string(format):
    """convert current time to string in required format"""
    time = datetime.now().strftime(format)
    return time


def convert_time_string(time, old_format, new_format):
    """convert string of time from one format to another
    e.g. from "17:30:29" to "173029"
    """
    time_object = datetime.strptime(time, old_format)
    new_time = time_object.strftime(new_format)
    return new_time


def highlight_text(text, fore, bg):
    """return highlighted text using rich markup"""
    return f"[{fore} on {bg}]{text}[/{fore} on {bg}]"
