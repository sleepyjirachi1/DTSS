def insert_table(rom_2, table_offset, table) -> None:
    """
    Inserts a table of bytes into a ROM

    :param table_offset: Offset of the table in the ROM
    :param table: A str of bytes (the table to insert)
    :return: None
    """
    with open(rom_2, 'r+b') as rom:
        rom.seek(table_offset)
        rom.write(table)
