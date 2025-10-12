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

class CrcParser(ParserBase):
    def __init__(self, read_file, show_pbar=False, log_level=logging.INFO, recovery_mode=True, write_unsafe=False):
        super().__init__(read_file, protocol='crc', show_pbar=show_pbar, log_level=log_level)
        # add custom variables here
        self.num_transport_packets = 0
        self.prev_crc = 0
        self.prev_trailer = bytearray()
        self.recovery_mode = recovery_mode    
        self.pid_crib = Counter(bytearray())
        
        self.previous_trailer = bytearray()
        self.cached_crc = None
        self.buffer = bytearray()
        self.aligned = False
        self.skipped = 0
        
        self.write_unsafe = write_unsafe
        
        pass
    
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

    def process_capture_old(self, data_field, UP_LEN=188):
        
        # self.logger.debug(data_field.hex())
        if len(data_field) % 188 == 0:
            self.logger.debug(f"data field length is modulo 188")
        self.logger.debug(f"TRAILER: {self.prev_trailer}")
        self.logger.debug(f"DATA FIELD: {data_field}")
        user_packet_stream = self.prev_trailer + data_field
        self.logger.debug(f"START OF USER PACKET STREAM")
        while len(user_packet_stream) >= UP_LEN:
            self.logger.debug(f"USER PACKET STREAM: {user_packet_stream.hex()}")
            self.logger.debug(f"USER PACKET STREAM: {user_packet_stream}")
            user_packet_with_crc = user_packet_stream[0:UP_LEN]
            self.logger.debug(f"ATTEMPTING {user_packet_with_crc}")
            user_packet = user_packet_with_crc[1:UP_LEN]
            if self.prev_crc == user_packet_with_crc[0]:
                self.logger.header(f"USER PACKET {MPEG_TS_SYNC_BYTE+user_packet}")
                self.write_protocol.write(MPEG_TS_SYNC_BYTE + user_packet)
                self.logger.debug(f"CRIB {user_packet_with_crc[1:3].hex()}")
                if self.recovery_mode: self.pid_crib.update(user_packet_with_crc[1:3])
                self.num_transport_packets += 1
            else: 
                # if self.recovery_mode:
                #     i = 0
                #     while i <= len(user_packet_stream)-2:
                #         if user_packet_stream[i:i+2] == self.pid_crib.most_common()[0][0] and i > 1:
                #             self.logger.debug(f"COMPARE {user_packet_stream[i:i+2].hex()} {self.pid_crib.most_common()[0][0].hex()}")
                #             del user_packet_stream[0:i-1]
                #             break
                #         else: 
                #             i+=1
                #             self.bytes_skipped += 1
                self.bytes_skipped += UP_LEN
            del user_packet_stream[0:UP_LEN]
            self.bytes_searched += 188
            self.prev_crc = Crc8DvbS2.calc(user_packet)
        
        self.prev_trailer = user_packet_stream

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
    
    crc = CrcParser(capture_file, log_level=log_level)
    crc.process_capture_file(capture_file)
    crc.log_status()
    crc.done_processing()

    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()
    