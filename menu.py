###   Menu   ###


from util import print_sf, input_sf


class Menu:
    def __init__(self, title, *options):
        self.title = title
        self.options = options

    def display(self):
        print_sf(self.title)
        for i in range(len(self.options)):
            print_sf(f'{i+1}. {self.options[i]}')
        print_sf(f'{i+2}. Exit')

    def get_option(self):
        while True:
            try:
                option = int(input_sf('Enter an option: '))
                if option in range(1, len(self.options) + 2):
                    return option
                else: raise ValueError
            except ValueError:
                print_sf('Invalid option')
