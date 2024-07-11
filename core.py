###   Core   ###


from pointers import LittleEndianPointer, PTR_SZ, BLANK_PTR


# General purpose memcpy function
def memcpy(dest, src, offset_dest, offset_src, length) -> None:
	"""
	Function to copy some bytes of defined length from src to dest.

	:param dest: Destination file
	:param src: Source file
    :param offset_dest: Offset in the destination file
    :param offset_src: Offset in the source file
	:param length: Number of bytes to copy
    :return: None
    """
    # Copy the data from the source file
	with open(src, 'rb') as source:
		source.seek(offset_src)
		data = source.read(length)

    # Write the data to the destination file
	with open(dest, 'r+b') as destination:
		destination.seek(offset_dest)
		destination.write(data)


# For use with wild encounters
def svrp_memcpy(dest, src, offset_dest, offset_src, length) -> LittleEndianPointer:
    """
    Function to copy some bytes and return the next pointer.

    :param dest: Destination file
    :param src: Source file
    :param offset_dest: Offset in the destination file
    :param offset_src: Offset in the source file
    :param length: Number of bytes to copy
    :return: The next pointer
    """
    # Copy the data and read the next pointer from the source file
    with open(src, 'rb') as source:
        source.seek(offset_src)
        data = source.read(length)
        ptr_next = source.read(PTR_SZ)

    # We do not appreciate blank pointers thank you very much
    if ptr_next != BLANK_PTR.raw:
        # Write the data to the destination file
        with open(dest, 'r+b') as destination:
            destination.seek(offset_dest)
            destination.write(data)

    # Return the next pointer
    return LittleEndianPointer(ptr_next).value


# For use with learnsets
def copy_table_of_ptrs_static(dest, src, count, table_offset) -> list:
    """
	Function to copy a table of n pointers from src to dest.

	:param dest: Destination file
	:param src: Source file
	:param count: Number of pointers in the table
	:param table_offset: Offset of the table in the ROM
	:return: A list of pointers
    """
    pointers = []
    with open(src, 'rb') as source:
        # Seek to the table offset
        source.seek(table_offset)

        # Loop through the table of n pointers
        for _ in range(count):

            # Read a pointer and add it to the list
            pointer = LittleEndianPointer(source.read(4))
            pointers.append(pointer.value)

            with open(dest, 'r+b') as destination:
                # Write the pointer into the destination file at the same location in memory
                destination.seek(table_offset)
                destination.write(pointer.raw)

            # Increment the table offset by 4 (since pointers are 4 bytes long)
            table_offset += 0x4

    return pointers


# For use with learnsets
def memcpy_block_static(dest, src, offset_src, length, end) -> None:
    """
    Function to copy a block of data from src to dest.

    :param dest: Destination file
    :param src: Source file
    :param offset_src: Offset in the source file
    :param length: Number of bytes to copy
    :param end: The end of the block
    :return: None
    """
    # Copy the data from the source file
    with open(src, 'rb') as source:
        # Seek the address pointed to by the pointer
        source.seek(offset_src)

        # While we haven't reached the end of the learnset
        while True:
            data = source.read(length)

            with open(dest, 'r+b') as destination:
                # Write the move to dest
                destination.seek(offset_src)
                destination.write(data)

            # Increment offset by length
            offset_src += length

            # Once we find the end of the block, we break
            if data == end: break
