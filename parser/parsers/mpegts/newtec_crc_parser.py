import logging
import os
import argparse
from tqdm import tqdm 
from collections import Counter
import math

from parser.config import plot_dir, write_dir, logs_dir
from parser.config import HEADER_LEVEL_NUM, PAYLOAD_LEVEL_NUM
from parser.config import MPEG_TS_SYNC_BYTE

from parser.utils.parser_utils import ParserBase

from crccheck.crc import Crc8DvbS2

class NewtecCrcParser(ParserBase):
    def __init__(self, read_file, show_pbar=False, log_level=logging.INFO, recovery_mode=True, write_unsafe=False):
        super().__init__(read_file, protocol='newtec.crc', show_pbar=show_pbar, log_level=log_level)
        # add custom variables here
        self.num_transport_packets = 0
        self.prev_crc = 0
        self.prev_trailer = bytearray()
        self.buffer = bytearray()
        
        self.write_unsafe = write_unsafe
        
        pass
    def reset(self):
        super().reset()
        self.num_transport_packets = 0
        self.prev_crc = 0
        self.prev_trailer = bytearray()
        self.buffer = bytearray()
    def process_capture(self, data_field, UP_LEN, SYNC_DISTANCE):

        buffer = bytearray()      
        pos = 0

        buffer = self.prev_trailer + data_field
        # buffer = data_field[:SYNC_DISTANCE] + self.prev_trailer + data_field[SYNC_DISTANCE:]
        self.logger.debug(f"data_field={len(data_field)}, upl={UP_LEN}, sync_d={SYNC_DISTANCE}")
        self.logger.debug(f"pos={pos}")
        self.logger.debug(f"sync_d={SYNC_DISTANCE}")
        self.logger.debug(f"data_field={data_field.hex()}")
        self.logger.debug(f"buffer={buffer.hex()}")
        self.logger.debug(f"len(buffer)={len(buffer)}")
        self.logger.debug(f"len(prev_trailer)={len(self.prev_trailer)}")
        self.logger.debug(f"{SYNC_DISTANCE} byte prefix, {math.floor((len(data_field)-SYNC_DISTANCE)/188)}x 188 byte user packets, {(len(data_field)-SYNC_DISTANCE)%188} byte trailer")
        
        
        while pos + 188 <= len(buffer):
            if SYNC_DISTANCE == 187 and pos==0:
                self.logger.debug(f"crc(data_field[:sync_d])={Crc8DvbS2.calc(data_field[:SYNC_DISTANCE])}")
                self.prev_crc = Crc8DvbS2.calc(data_field[:SYNC_DISTANCE])
                self.write_protocol.write(MPEG_TS_SYNC_BYTE+data_field[:SYNC_DISTANCE])
            elif SYNC_DISTANCE + len(self.prev_trailer) == 188 and pos==0:
                self.logger.debug(f"crc(data_field[1:prev_crc+sync_d])={Crc8DvbS2.calc(buffer[1:188])}")
                self.prev_crc = Crc8DvbS2.calc(buffer[1:188])
                self.write_protocol.write(MPEG_TS_SYNC_BYTE+buffer[1:188])
                
            
            if pos < (len(self.prev_trailer) + SYNC_DISTANCE):
                # self.logger.debug(f"test={Crc8DvbS2.calc(buffer[pos:pos+(len(self.prev_trailer) + SYNC_DISTANCE)])}")
                # self.logger.debug(f"skipping {buffer[pos:len(self.prev_trailer) + SYNC_DISTANCE].hex()}")
                self.logger.debug(f"setting pos to start of user packet stream pos={pos}")
                pos = len(self.prev_trailer) + SYNC_DISTANCE
            else: 
                self.logger.debug(f"{len(buffer[pos:pos+188])} bytes: {buffer[pos:pos+188].hex()}")
                self.logger.debug(f"crc={buffer[pos]}, prev_crc={self.prev_crc}")
                if self.prev_crc == buffer[pos]:
                    self.logger.debug(f"CRC SUCCESS")
                    self.write_protocol.write(MPEG_TS_SYNC_BYTE+buffer[pos+1:pos+188])
                    self.bytes_searched += 188
                    self.num_transport_packets += 1

                else: 
                    self.logger.debug(f"CRC FAIL")
                    if self.write_unsafe:
                        self.write_protocol.write(MPEG_TS_SYNC_BYTE+buffer[pos+1:pos+188])
                    self.bytes_skipped += 188
                    self.bytes_searched += 188
                self.prev_crc=Crc8DvbS2.calc(buffer[pos+1:pos+188])
                self.logger.debug(f"new prev_crc={self.prev_crc}")
                pos += 188
                
            # self.logger.debug(f"{len(buffer[pos:pos+188])} bytes: {buffer[pos:pos+188].hex()}")
        self.logger.debug(f"{len(buffer[pos:])} bytes: {buffer[pos:].hex()}")
        self.prev_trailer = buffer[pos:]

    def process_capture_file(self, capture_file, preview_len=None):
        super().process_capture_file(capture_file, preview_len)
    def done_processing(self):
        super().done_processing()
    def log_status(self, logger=None):
        super().log_status(logger)  
        logger = self.logger if logger == None else logger
        logger.info(f"{self.num_transport_packets} crc encoded transport packets were found")



def main():
    parser = argparse.ArgumentParser(description="Process TODO capture files with custom logging verbosity.")
    parser.add_argument("capture_file", help="Path to the input raw capture file.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="Increase logging verbosity. Default: INFO. -v: HEADER. -vv: DEBUG. -vvv: PAYLOAD (most verbose).")
    
    args = parser.parse_args() # Parse command-line arguments

    if args.verbose == 0:
        log_level = logging.INFO
    elif args.verbose == 1:
        log_level = HEADER_LEVEL_NUM # Use the custom level constant
    elif args.verbose == 2:
        log_level = PAYLOAD_LEVEL_NUM # Use the custom level constant
    else: # args.verbose >= 3
        log_level = logging.DEBUG 

    for directory in [logs_dir, write_dir, plot_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}") # Print before logger is fully initialized to console

    capture_file = args.capture_file
    
    crc = NewtecCrcParser(capture_file, log_level=log_level)
    crc.process_capture_file(capture_file)
    crc.log_status()
    crc.done_processing()

    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()
    