###   Util   ###


from time import sleep


def print_sf(text, delay=0.0025, end=True) -> None:
    """
    Prints text with a delay between each letter.

    :param text: The text to print
    :param delay: The delay between each letter
    :param end: Whether to end the line after printing
    :return: None
    """
    for letter in text:
        print(letter, end='', flush=True)
        sleep(delay)
    if end: print()


def input_sf(prompt, delay=0.0025) -> None:
    """
    Prints a prompt with a delay between each letter, then returns user input.
    
    :param prompt: The prompt to print
    :param delay: The delay between each letter
    :return: The user input
    """
    print_sf(prompt, delay, end=False)
    return input()
