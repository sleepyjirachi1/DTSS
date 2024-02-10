###   Extract   ###


def extract_table(file, table_offset, entry_length, table_entries) -> str:
    """
    Extracts a table of bytes from a ROM

    :param table_offset: Offset of the table in the ROM
    :param entry_length: Length of each entry in the table (in hex)
    :param table_entries: Number of entries in the table
    :return: A str of bytes (the original table)
    """
    table_size = entry_length * table_entries
    with open(file, 'rb') as rom:
        rom.seek(table_offset)
        table = rom.read(table_size)
    return table
