from time import sleep


def print_sf(text, delay=0.025, end=True):
    """Prints text with a delay between each letter."""
    for letter in text:
        print(letter, end='', flush=True)
        sleep(delay)
    if end: print()


def input_sf(prompt, delay=0.025):
    """Prints a prompt with a delay between each letter, then returns user input."""
    print_sf(prompt, delay, end=False)
    return input()
