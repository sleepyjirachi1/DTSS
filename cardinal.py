###    Cardinal    ###


import concurrent.futures as Threading
from util import print_sf
from pointers import LittleEndianPointer
from core import memcpy, copy_table_of_ptrs_static
from copying import copy_wild_encounter_tables, visit_and_copy_learnset


NO_OF_MONS = 0x4F4


class TransferCardinal:
    def __init__(self):
        self.__rom_1 = 'test.gba'
        self.__rom_2 = 'BPRE0.gba'

    def __transfer_pokemon_names(self):
        """
        Transfer the pokemon names from rom_1 to rom_2.
        """
        print_sf("Transferring Pokemon Names...")
        offset = 0x16184C0
        memcpy(self.__rom_2, self.__rom_1, offset, offset, 0xD * NO_OF_MONS)

    def __transfer_trainer_data(self):
        """
        Transfer the trainer data from rom_1 to rom_2.
        """
        print_sf("Transferring Trainer Data...")

        # Refactor this
        TRAINER_TABLE_OFFSET = 0x23EAC8

        struct_t = {
            0: 8,
            1: 8,
            2: 16,
            3: 16,
        }

        pokemon_ptrs = []
        
        for _ in range(0x2E6 - 1):

            with open(self.__rom_1, 'rb') as source:
                source.seek(TRAINER_TABLE_OFFSET)
                trainer_stuff = source.read(0x4)
                source.read(0x1C)
                count = source.read(0x4)
                ptr = LittleEndianPointer(source.read(0x4))

            if ptr.raw != b'\x00\x00\x00\x00':
                offset = int(ptr.value, 16)
                pokemon_ptrs.append((offset, count[0], struct_t[trainer_stuff[0]]))

            memcpy(self.__rom_2, self.__rom_1, TRAINER_TABLE_OFFSET, TRAINER_TABLE_OFFSET, 0x40)

            TRAINER_TABLE_OFFSET += 0x28

        for offset, count, struct_sz in pokemon_ptrs: memcpy(self.__rom_2, self.__rom_1, offset, offset, count * struct_sz)

    def __transfer_wild_encounter_tables(self):
        """
        Transfer the wild encounter tables from rom_1 to rom_2.
        """
        print_sf("Transferring Wild Encounter Tables...")

        # Terrain types
        terrain_types = {
            'grass': 0xC,
            'surf': 0x5,
            'rock_smash': 0x5,
            'fishing': 0xA
        }

        # Copy the wild encounter tables
        copy_wild_encounter_tables(self.__rom_2, self.__rom_1, terrain_types, 133, 0x3C9CB8)

    def __transfer_learnsets(self):
        """Transfer the learnsets from rom_1 to rom_2."""
        print_sf("Transferring Learnsets...")

        # Copy the learnset pointers table
        pointers = copy_table_of_ptrs_static(self.__rom_2, self.__rom_1, NO_OF_MONS, 0x19B9E14)

        # WARNING: Never change the max workers unless you know exactly what you are doing
        with Threading.ThreadPoolExecutor(max_workers=5) as threads:
            threads.map(visit_and_copy_learnset, pointers)

    def __transfer_base_stats(self):
        """
        Transfer the base stats from rom_1 to rom_2.
        """
        print_sf("Transferring Base Stats...")
        offset = 0x19778E0
        memcpy(self.__rom_2, self.__rom_1, offset, offset, 0x1C * NO_OF_MONS)

    def __transfer_evolutions(self):
        """Transfer the evolutions from rom_1 to rom_2."""
        print_sf("Transferring Evolutions...")
        offset = 0x198A2A0
        memcpy(self.__rom_2, self.__rom_1, offset, offset, 0x80 * NO_OF_MONS)

    @property
    def get_transfer_methods(self):
        return {'pokemon_names': self.__transfer_pokemon_names,
                'trainer_data': self.__transfer_trainer_data,
                'wild_encounter_tables': self.__transfer_wild_encounter_tables,
                'learnsets': self.__transfer_learnsets,
                'base_stats': self.__transfer_base_stats,
                'evolutions': self.__transfer_evolutions}

    def transfer_all(self):
        """Take all uncalled methods from the method dictionary and call them."""
        for method in self.get_transfer_methods.values():
            method()
