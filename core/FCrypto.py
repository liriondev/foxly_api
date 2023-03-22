from ctypes import *
import os
import ctypes, struct

class WFLib:

    def __init__(self, address):

        lib = CDLL(os.path.abspath("foxly_api/libs/fcrypto-amd64.so"))

        lib.connection_new.argtypes = [c_char_p]
        lib.connection_new.restype = c_void_p

        lib.connection_send_data.argtypes = [c_void_p, c_char_p, c_char_p]
        lib.connection_send_data.restype = None

        lib.connection_read_data.argtypes = [c_void_p]
        lib.connection_read_data.restype = c_char_p

        self.conn = lib.connection_new(address.encode())
        self.lib = lib
        self.hash: str
    
    def read_data(self) -> bytes:
        data = ctypes.string_at(self.lib.connection_read_data(self.conn))

        buf = bytearray(data)
        pos = len(buf) - 1

        val = buf[pos]

        while ((0x01 <= val) and (val <= 0x10)):
            buf[pos] = 0x00
            pos = pos - 1
            if (val != buf[pos]):
                break

        if (pos != len(buf) - 1):
            length = len(buf) - pos - 1
            buf = buf[0:len(buf) - length]

        return buf


    
    def send_data(self, data):
        self.lib.connection_send_data(self.conn, data.encode(), self.hash.encode())
