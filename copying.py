###   Copying   ###


from pointers import LittleEndianPointer, PTR_SZ, NULL_PTR, BLANK_PTR
from core import memcpy, svrp_memcpy, memcpy_block_static


def copy_trainer_tables(dest, src, num_trainers, struct_t, offset) -> None:
		# Make a list for the pokemon data pointers
        pokemon_ptrs = []

        for _ in range(num_trainers):

            # Read the trainer data
            with open(src, 'rb') as source:
                source.seek(offset)
                trainer_stuff = source.read(0x4)
                source.read(0x1C)
                count = source.read(0x4)
                ptr = LittleEndianPointer(source.read(0x4))

            # We don't want to copy null pointers
            if ptr.raw != NULL_PTR:
				# Convert the pointer to a hex string
                pointer = int(ptr.value, 16)
                pokemon_ptrs.append((pointer, count[0], struct_t[trainer_stuff[0]]))

            # Let's memcpy the trainer data!
            memcpy(dest, src, offset, offset, 0x28)

            # Increment the table offset by 40 bytes (trainer data size)
            offset += 0x28

        # Loop through the pokemon data and write it to corresponding pointers
        for ofs, count, struct_sz in pokemon_ptrs: memcpy(dest, src, ofs, ofs, count * struct_sz)


def copy_and_write_wild_header(dest, src, ptr) -> LittleEndianPointer:
    # Convert a hexadecimal address (string) to an integer
    offset_src = int(ptr, 16)

    # Let's memcpy this now and return a pointer!
    return svrp_memcpy(dest, src, offset_src, offset_src, 0x4)


def visit_and_copy_wild_encounters(dest, src, ptr, data_length) -> None:
    """
    Copies the wild encounter data from src to dest at the location pointer to by ptr.

    :param dest: The destination file.
    :param src: The source file.
    :param ptr: The offset of the wild encounter data in the source file.
    :param data_length: The length of the wild encounter data.
    """
    # Convert a hexadecimal address (string) to an integer
    offset_src = int(ptr, 16)

    # Let's memcpy this now!
    memcpy(dest, src, offset_src, offset_src, data_length * 0x4)


def copy_wild_encounter_tables(dest, src, terrain_types, num_tables, offset) -> None:
	"""
	Copies the wild encounter tables from src to dest.

	:param dest: The destination file.
	:param src: The source file.
	:param terrain_types: The terrain types and their corresponding lengths.
	:param num_tables: The number of wild encounter tables to copy.
	:param offset: The offset to the start of the wild encounter tables in src.
	:return: None
	"""
	with open(src, 'rb') as source:
		source.seek(offset)

		for _ in range(num_tables):
			source.read(PTR_SZ)
			grass_ptr = LittleEndianPointer(source.read(PTR_SZ))
			surf_ptr = LittleEndianPointer(source.read(PTR_SZ))
			rock_smash_ptr = LittleEndianPointer(source.read(PTR_SZ))
			fishing_ptr = LittleEndianPointer(source.read(PTR_SZ))

			if grass_ptr.raw != NULL_PTR:
				wild_data_pointer = copy_and_write_wild_header(dest, src, grass_ptr.value)
				if wild_data_pointer != BLANK_PTR.value:
					visit_and_copy_wild_encounters(dest, src, wild_data_pointer, terrain_types['grass'])

			if surf_ptr.raw != NULL_PTR:
				wild_data_pointer = copy_and_write_wild_header(dest, src, surf_ptr.value)
				if wild_data_pointer != BLANK_PTR.value:
					visit_and_copy_wild_encounters(dest, src, wild_data_pointer, terrain_types['surf'])

			if rock_smash_ptr.raw != NULL_PTR:
				wild_data_pointer = copy_and_write_wild_header(dest, src, rock_smash_ptr.value)
				if wild_data_pointer != BLANK_PTR.value:
					visit_and_copy_wild_encounters(dest, src, wild_data_pointer, terrain_types['rock_smash'])

			if fishing_ptr.raw != NULL_PTR:
				wild_data_pointer = copy_and_write_wild_header(dest, src, fishing_ptr.value)
				if wild_data_pointer != BLANK_PTR.value:
					visit_and_copy_wild_encounters(dest, src, wild_data_pointer, terrain_types['fishing'])


def visit_and_copy_learnset(ptr, dest='BPRE0.gba', src='test.gba') -> None:
    """
	Copies the data for a single learnset from src to dest.
    The learnset data is pointed to by the address given by ptr.

    :param ptr: The pointer to the learnset data in the source ROM.
    :param dest: The destination file.
    :param src: The source file.
    :return: None
    """
    # Convert a hexadecimal address (string) to an integer
    offset_src = int(ptr, 16)

    # Let's memcpy this now!
    memcpy_block_static(dest, src, offset_src, 0x3, b'\x00\x00\xff')
