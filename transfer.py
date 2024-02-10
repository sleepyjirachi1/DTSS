###   Main Control Script   ###


# Imports (System bound)
import concurrent.futures as Threading


# Imports (Locally bound)
from util import print_sf
from extract import extract_table
from insert import insert_table
from copying import copy_table_of_pointers, visit_and_copy_learnset, visit_and_copy_icon_sprite
from copying import visit_and_copy_wild_encounters, copy_and_write_wild_header
from pointers import LittleEndianPointer, NULL_PTR, NOT_A_PTR
from menu import Menu


###    Cardinal    ###
class TransferCardinal:
    """We shouldn't expect a crash, in the case of a crash, we might need to save the current state of the transfer."""
    def __init__(self):
        self.__rom_1 = 'test.gba'
        self.__rom_2 = 'BPRE0.gba'

    def __transfer_pokemon_names(self):
        """Transfer the pokemon names from rom_1 to rom_2."""
        print_sf("Transferring Pokemon Names...")

        table_offset = 0x16184C0
        entry_length = 0xD
        table_entries = 0x4F4
        table = extract_table(self.__rom_1, table_offset, entry_length, table_entries)
        insert_table(self.__rom_2, table_offset, table)

    def __transfer_icon_sprites(self):
        """Transfer the icon sprites from rom_1 to rom_2."""
        print_sf("Transferring Icon Sprites...")

        # Table of pointers for icon sprites
        table_offset = 0x19B7180
        pointers = copy_table_of_pointers(self.__rom_1, self.__rom_2, table_offset)

        # WARNING: Never change the max workers unless you know exactly what you are doing
        with Threading.ThreadPoolExecutor(max_workers=4) as threads:
            threads.map(visit_and_copy_icon_sprite, pointers)

        # Icon palette index table
        table_offset = 0x19B6C8C
        entry_length = 0x1
        table_entries = 0x4F4
        table = extract_table(self.__rom_1, table_offset, entry_length, table_entries)
        insert_table(self.__rom_2, table_offset, table)

    def __transfer_wild_encounter_tables(self):
        """Transfer the wild encounter tables from rom_1 to rom_2."""
        print_sf("Transferring Wild Encounter Tables...")

        # Definitions
        table_offset = 0x3C9CB8
        header_length = 0x4
        terrain_types = {
            'grass': 0xC,
            'surf': 0x5,
            'rock_smash': 0x5,
            'fishing': 0xA
        }

        # Will work on commenting and cleaning up this nasty code later
        # It doesn't really belong in the main control script
        with open(self.__rom_1, 'rb') as rom:
            rom.seek(table_offset)

            for _ in range(133):
                rom.read(header_length)
                grass_ptr = LittleEndianPointer(rom.read(4))
                surf_ptr = LittleEndianPointer(rom.read(4))
                rock_smash_ptr = LittleEndianPointer(rom.read(4))
                fishing_ptr = LittleEndianPointer(rom.read(4))

                if grass_ptr.raw != NULL_PTR:
                    wild_data_pointer = copy_and_write_wild_header(grass_ptr.value, self.__rom_1, self.__rom_2)
                    if wild_data_pointer != NOT_A_PTR.value:
                        visit_and_copy_wild_encounters(wild_data_pointer, terrain_types['grass'], self.__rom_1, self.__rom_2)

                if surf_ptr.raw != NULL_PTR:
                    wild_data_pointer = copy_and_write_wild_header(surf_ptr.value, self.__rom_1, self.__rom_2)
                    if wild_data_pointer != NOT_A_PTR.value:
                        visit_and_copy_wild_encounters(wild_data_pointer, terrain_types['surf'], self.__rom_1, self.__rom_2)

                if rock_smash_ptr.raw != NULL_PTR:
                    wild_data_pointer = copy_and_write_wild_header(rock_smash_ptr.value, self.__rom_1, self.__rom_2)
                    if wild_data_pointer != NOT_A_PTR.value:
                        visit_and_copy_wild_encounters(wild_data_pointer, terrain_types['rock_smash'], self.__rom_1, self.__rom_2)

                if fishing_ptr.raw != NULL_PTR:
                    wild_data_pointer = copy_and_write_wild_header(fishing_ptr.value, self.__rom_1, self.__rom_2)
                    if wild_data_pointer != NOT_A_PTR.value:
                        visit_and_copy_wild_encounters(wild_data_pointer, terrain_types['fishing'], self.__rom_1, self.__rom_2)

    def __transfer_learnsets(self):
        """Transfer the learnsets from rom_1 to rom_2."""
        print_sf("Transferring Learnsets...")

        table_offset = 0x19B9E14
        pointers = copy_table_of_pointers(self.__rom_1, self.__rom_2, table_offset)

        # WARNING: Never change the max workers unless you know exactly what you are doing
        with Threading.ThreadPoolExecutor(max_workers=4) as threads:
            threads.map(visit_and_copy_learnset, pointers)

    def __transfer_base_stats(self):
        """Transfer the base stats from rom_1 to rom_2."""
        print_sf("Transferring Base Stats...")

        table_offset = 0x19778E0
        entry_length = 0x1C
        table_entries = 0x4F4
        table = extract_table(self.__rom_1, table_offset, entry_length, table_entries)
        insert_table(self.__rom_2, table_offset, table)

    def __transfer_evolutions(self):
        """Transfer the evolutions from rom_1 to rom_2."""
        print_sf("Transferring Evolutions...")

        table_offset = 0x198A2A0
        entry_length = 0x80
        table_entries = 0x4F4
        table = extract_table(self.__rom_1, table_offset, entry_length, table_entries)
        insert_table(self.__rom_2, table_offset, table)

    @property
    def get_transfer_methods(self):
        return {'pokemon_names': self.__transfer_pokemon_names,
                'icon_sprites': self.__transfer_icon_sprites,
                'wild_encounter_tables': self.__transfer_wild_encounter_tables,
                'learnsets': self.__transfer_learnsets,
                'base_stats': self.__transfer_base_stats,
                'evolutions': self.__transfer_evolutions}

    def transfer_all(self):
        """Take all uncalled methods from the method dictionary and call them."""
        for method in self.get_transfer_methods.values():
            method()


if __name__ == '__main__':
    # Thanks Copilot!!! <3, You saved me countless hours!

    # Init the transfer cardinal
    transfer_cardinal = TransferCardinal()

    # Main Menu
    menu = Menu(
        "What would you like to transfer?",
        "Transfer" + " Pokemon Names",
        "Transfer" + " Icon Sprites",
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
        2: "icon_sprites",
        3: "wild_encounter_tables",
        4: "learnsets",
        5: "base_stats",
        6: "evolutions",
    }

    # I like the use of a dictionary here, it's a nice touch.
    # It's a good way to avoid a bunch of if statements.
    # Exception handling is done by the menu so we don't need to worry about that.
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
