from pointers import LittleEndianPointer, NOT_A_PTR


def copy_table_of_pointers(file_1, file_2, table_offset):
    """
    Copies a table of pointers from one ROM to another
    The table of pointers must be terminated by a null pointer

    :param table_offset: Offset of the table of pointers in the ROM
    :return: A list of pointers
    """
    pointers = []
    with open(file_1, 'rb') as rom:
        rom.seek(table_offset)
        # Screw this I don't think it's FF terminated
        for _ in range(1268):
            pointer = LittleEndianPointer(rom.read(4))
            pointers.append(pointer.value)
            with open(file_2, 'r+b') as rom2:
                rom2.seek(table_offset)
                rom2.write(pointer.raw)
            table_offset += 0x4
    return pointers


def visit_and_copy_learnset(pointer, file_1='test.gba', file_2='BPRE0.gba'):
    # Convert a hexadecimal address (string) to an integer
    address = int(pointer, 16)

    # Read the learnset data from the pointer
    with open(file_1, 'rb') as rom:
        rom.seek(address)

        while True:
            data = rom.read(3)

            # Write the learnset data to the target ROM
            with open(file_2, 'r+b') as rom2:
                rom2.seek(address)
                rom2.write(data)

            address += 0x3

            # Once we find the end of the learnset, we break
            if data == b'\x00\x00\xff':
                break


def visit_and_copy_icon_sprite(pointer, file_1='test.gba', file_2='BPRE0.gba'):
    # Convert a hexadecimal address (string) to an integer
    address = int(pointer, 16)

    # Read the sprite data from the pointer
    with open(file_1, 'rb') as rom:
        rom.seek(address)
        data = rom.read(0x420)

        # Write the sprite data to the target ROM
        with open(file_2, 'r+b') as rom2:
            rom2.seek(address)
            rom2.write(data)


def copy_and_write_wild_header(pointer, file_1, file_2):
    # Convert a hexadecimal address (string) to an integer
    address = int(pointer, 16)

    # Read the wild header data from the pointer
    with open(file_1, 'rb') as rom:
        rom.seek(address)
        data = rom.read(8)
        ptr_next = data[4:]

    # We do not appreciate rogue pointers thank you very much
    if ptr_next != NOT_A_PTR.raw:
        # Write the wild header data to the target ROM
        with open(file_2, 'r+b') as rom:
            rom.seek(address)
            rom.write(data)

    return LittleEndianPointer(ptr_next).value


def visit_and_copy_wild_encounters(pointer, data_length, file_1, file_2):
    # Convert a hexadecimal address (string) to an integer
    address = int(pointer, 16)

    # Read the wild encounter data from the pointer
    with open(file_1, 'rb') as rom:
        rom.seek(address)
        wild_data = rom.read(data_length * 0x4)

    # Write the wild encounter data to the target ROM
    with open(file_2, 'r+b') as rom:
        rom.seek(address)
        rom.write(wild_data)
