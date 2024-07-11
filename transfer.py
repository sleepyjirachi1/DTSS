###   Main Control Script   ###


from cardinal import TransferCardinal
from menu import Menu
from util import print_sf


if __name__ == '__main__':
    # Init the transfer cardinal
    transfer_cardinal = TransferCardinal()

    # Main Menu
    menu = Menu(
        "What would you like to transfer?",
        "Transfer" + " Pokemon Names",
        "Transfer" + " Trainer Data",
        "Transfer" + " Wild Encounter Tables",
        "Transfer" + " Learnsets",
        "Transfer" + " Base Stats",
        "Transfer" + " Evolutions",
        "Transfer All"
    )
    menu.display()
    print()
    option = menu.get_option()

    options = {
        1: "pokemon_names",
        2: "trainer_data",
        3: "wild_encounter_tables",
        4: "learnsets",
        5: "base_stats",
        6: "evolutions",
    }

    # Perform the selected transfer option
    if option == 7:
        print()
        transfer_cardinal.transfer_all()
        print_sf("Transfer Complete")
    elif option == 8:
        exit()
    elif options[option] in transfer_cardinal.get_transfer_methods:
        print()
        transfer_cardinal.get_transfer_methods[options[option]]()
        print_sf("Transfer Complete")
