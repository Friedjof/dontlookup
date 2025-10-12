import logging
import os
import argparse

from parser.config import plot_dir, write_dir, logs_dir, promising_dir
from parser.config import HEADER_LEVEL_NUM, PAYLOAD_LEVEL_NUM, PREVIEW_LENGTH
from parser.utils.parser_utils import ParserResults

from parser.parsers.dvbs2.dvbs2_parser import DVBS2Parser
from parser.parsers.mpegts.mpegts_parser import MpegtsParser
from parser.parsers.mpegts.crc_parser import CrcParser
from parser.parsers.mpegts.generic_crc_parser import GenericCrcParser
from parser.parsers.mpegts.newtec_crc_parser import NewtecCrcParser

def main():
    parser = argparse.ArgumentParser(description="Process DVBS2 capture files with custom logging verbosity.")
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
    
    
    DVBS2 = DVBS2Parser(capture_file, log_level=log_level, show_pbar=True)
    MPEGTS = MpegtsParser(DVBS2.protocol_file, log_level=log_level, show_pbar=True)
    CRC_MPEGTS = GenericCrcParser(DVBS2.protocol_file, log_level=log_level, write_unsafe=True)
    NEWTEC_CRC = NewtecCrcParser(DVBS2.protocol_file, log_level=log_level, write_unsafe=True)
    
    DVBS2.add_parser(CRC_MPEGTS)
    DVBS2.add_parser(NEWTEC_CRC)
    
    DVBS2.process_capture_file(capture_file, PREVIEW_LENGTH)
    DVBS2.log_status()
    DVBS2.done_processing()
    
    MPEGTS.process_capture_file(DVBS2.protocol_file, PREVIEW_LENGTH)
    MPEGTS.log_status()
    MPEGTS.done_processing()
    
    CRC_MPEGTS.log_status()
    CRC_MPEGTS.done_processing()
    NEWTEC_CRC.log_status()
    NEWTEC_CRC.done_processing()
    
    results = ParserResults()
    results.start_file(capture_file)
    
    if DVBS2.get_compliance() > .90:
        results.add_parser("DVBS2", compliance=DVBS2.get_compliance())
        if NEWTEC_CRC.get_compliance() > .90 and NEWTEC_CRC.bytes_skipped <= CRC_MPEGTS.bytes_skipped:
            print(NEWTEC_CRC.protocol_file)
            DVBS2.reset()
            NEWTEC_CRC.reset()
            DVBS2.add_parser(NEWTEC_CRC)
            DVBS2.process_capture_file(capture_file)
            DVBS2.log_status()
            DVBS2.done_processing()
            os.system(f"mv '{NEWTEC_CRC.protocol_file}' {promising_dir}")
            results.add_parser("NEWTEC_CRC", compliance=NEWTEC_CRC.get_compliance())
            
        elif CRC_MPEGTS.get_compliance() > .90:
            print(CRC_MPEGTS.protocol_file)
            DVBS2.reset()
            CRC_MPEGTS.reset()
            DVBS2.add_parser(CRC_MPEGTS)
            DVBS2.process_capture_file(capture_file)
            DVBS2.log_status()
            DVBS2.done_processing()
            os.system(f"mv '{CRC_MPEGTS.protocol_file}' {promising_dir}")
            
            results.add_parser("CRC_MPEGTS", compliance=CRC_MPEGTS.get_compliance())

        elif MPEGTS.get_compliance() > 0.90:
            print(MPEGTS.protocol_file)
            DVBS2.reset()
            MPEGTS.reset()
            
            DVBS2.process_capture_file(capture_file)
            DVBS2.log_status()
            DVBS2.done_processing()
            
            MPEGTS.process_capture_file(DVBS2.protocol_file)
            MPEGTS.log_status()
            MPEGTS.done_processing()
            os.system(f"mv '{MPEGTS.protocol_file}' {promising_dir}")
            
            results.add_parser("MPEGTS", compliance=MPEGTS.get_compliance())
            
            
    results.finalize_file()        
    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()