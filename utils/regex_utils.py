import re
def match_regex(input_str: str, pattern: str) -> bool:
    """
    Checks if the input string matches the regex pattern with re.
    
    Args:
        input_str (str): The input string to check.
        pattern (str): The regex pattern to check with.
    
    Returns:
        bool: True if match, False if not.
    """
    return bool(re.match(pattern, input_str))

USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9]+$')
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d).{4,}$')