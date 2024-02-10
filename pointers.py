###   Pointers   ###


class LittleEndianPointer:
    def __init__(self, _bytes):
        self.__bytes = _bytes

    def convert_from_bytes(self):
        value= int.from_bytes(self.__bytes, byteorder='little')
        addr_no_prefix = format(value, 'X')
        return '0x1' + addr_no_prefix[1:] if addr_no_prefix[0] == '9' else '0x' + addr_no_prefix[1:]

    @property
    def raw(self):
        return self.__bytes

    @property
    def value(self):
        return self.convert_from_bytes()


NULL_PTR = b'\x00\x00\x00\x00'
NOT_A_PTR = LittleEndianPointer(b'\xFF\xFF\xFF\xFF')
