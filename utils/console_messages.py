from datetime import datetime
import inspect

_messages_log = []
def console_message(level: str, contents: str, log: bool = True):
    """
    Generate and print a formatted message with a timestamp \n
    and the current caller's name. Optionally log the message.
    Args:
        level (str): The log level (e.g. 'WARN', 'ERROR').
        contents (str): The message contents.
        log (bool): Optional message log. Default is True.
    """
    frame = inspect.currentframe().f_back # get caller's name
    name = frame.f_code.co_name
    message = f"[{datetime.now().strftime("%H:%M:%S")}] [{level} / {name}]: {contents}"
    if log:
        _messages_log.append(message)
    print(message)

def console_message_log() -> tuple:
    """
    Return all of the console message logs.
    """
    return tuple(_messages_log)