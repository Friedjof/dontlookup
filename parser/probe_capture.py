import logging
import os
import argparse

from parser.config import plot_dir, write_dir, logs_dir, promising_dir
from parser.config import HEADER_LEVEL_NUM, PAYLOAD_LEVEL_NUM, PREVIEW_LENGTH

from parser.parsers.dvbs2.dvbs2_parser import DVBS2Parser
from parser.parsers.mpegts.mpegts_parser import MpegtsParser
from parser.parsers.mpegts.generic_crc_parser import GenericCrcParser
from parser.parsers.mpegts.newtec_crc_parser import NewtecCrcParser
from parser.parsers.ip.ip_parser import IPv4Parser
from parser.parsers.gse.gse_parser import StandardLenSplitCacheGSEParser, StandardLenStandardCacheGSEParser, Len2SplitCacheGSEParser, Len2StandardCacheGSEParser
from parser.parsers.rev.rev_parser import Reverse_Parser

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
    MPEGTS = MpegtsParser(capture_file, log_level=log_level, show_pbar=True)
    IP = IPv4Parser(capture_file, log_level=log_level, show_pbar=True)
    
    
    DVBS2_MPEGTS = MpegtsParser(DVBS2.protocol_file, log_level=log_level, show_pbar=True)
    DVBS2_CRC_MPEGTS = GenericCrcParser(DVBS2.protocol_file, log_level=log_level, write_unsafe=True)
    DVBS2_NEWTEC_CRC = NewtecCrcParser(DVBS2.protocol_file, log_level=log_level, write_unsafe=True)
    DVBS2_IP = IPv4Parser(DVBS2.protocol_file, log_level=log_level, show_pbar=True)
    DVBS2_STDLEN_SPLITCACHE_GSE = StandardLenSplitCacheGSEParser(DVBS2.protocol_file, protocol='stdlen.split.gse', log_level=log_level)
    DVBS2_STDLEN_STDCACHE_GSE = StandardLenStandardCacheGSEParser(DVBS2.protocol_file, protocol='stdlen.std.gse', log_level=log_level)
    DVBS2_LEN2_SPLITCACHE_GSE = Len2SplitCacheGSEParser(DVBS2.protocol_file, protocol='len2.split.gse', log_level=log_level)
    DVBS2_LEN2_STDCACHE_GSE = Len2StandardCacheGSEParser(DVBS2.protocol_file, protocol='len2.std.gse', log_level=log_level)
    DVBS2_REV = Reverse_Parser(DVBS2.protocol_file, log_level=log_level)
    DVBS2_REV_IP = IPv4Parser(DVBS2_REV.protocol_file, log_level=log_level, show_pbar=True)
    DVBS2_STDLEN_SPLITCACHE_GSE_IP = IPv4Parser(DVBS2_STDLEN_SPLITCACHE_GSE.protocol_file, log_level=log_level, show_pbar=True)
    DVBS2_STDLEN_STDCACHE_GSE_IP = IPv4Parser(DVBS2_STDLEN_STDCACHE_GSE.protocol_file, log_level=log_level, show_pbar=True)
    DVBS2_LEN2_SPLITCACHE_GSE_IP = IPv4Parser(DVBS2_LEN2_SPLITCACHE_GSE.protocol_file, log_level=log_level, show_pbar=True)
    DVBS2_LEN2_STDCACHE_GSE_IP = IPv4Parser(DVBS2_LEN2_STDCACHE_GSE.protocol_file, log_level=log_level, show_pbar=True)
    # DVBS2_LEN2_SPLITCACHE_GSE_MPEGTS = MpegtsParser(DVBS2_LEN2_SPLITCACHE_GSE.protocol_file, log_level=log_level, show_pbar=True)
    
    DVBS2.add_parser(DVBS2_CRC_MPEGTS)
    DVBS2.add_parser(DVBS2_NEWTEC_CRC)
    DVBS2.add_parser(DVBS2_STDLEN_SPLITCACHE_GSE)
    DVBS2.add_parser(DVBS2_STDLEN_STDCACHE_GSE)
    DVBS2.add_parser(DVBS2_LEN2_SPLITCACHE_GSE)
    DVBS2.add_parser(DVBS2_LEN2_STDCACHE_GSE)
    # DVBS2.add_parser(DVBS2_REV)

    
    # runs on the capture file directly
    DVBS2.process_capture_file(capture_file, PREVIEW_LENGTH)
    DVBS2.log_status()
    DVBS2.done_processing()
    
    MPEGTS.process_capture_file(capture_file, PREVIEW_LENGTH)
    MPEGTS.log_status()
    MPEGTS.done_processing()
    
    IP.process_capture_file(capture_file, PREVIEW_LENGTH)
    IP.log_status()
    IP.done_processing()
    
    # runs after the dvbs2 parser
    
    DVBS2_MPEGTS.process_capture_file(DVBS2.protocol_file, PREVIEW_LENGTH)
    DVBS2_MPEGTS.log_status()
    DVBS2_MPEGTS.done_processing()
    
    DVBS2_IP.process_capture_file(DVBS2.protocol_file, PREVIEW_LENGTH)
    DVBS2_IP.log_status()
    DVBS2_IP.done_processing()
    
    DVBS2_REV.process_capture_file(DVBS2.protocol_file, PREVIEW_LENGTH)
    DVBS2_REV.log_status()
    DVBS2_REV.done_processing()
    

    # runs during the dvbs2 parser on each bbframe
    DVBS2_CRC_MPEGTS.log_status()
    DVBS2_CRC_MPEGTS.done_processing()
    
    DVBS2_NEWTEC_CRC.log_status()
    DVBS2_NEWTEC_CRC.done_processing()
    
    DVBS2_STDLEN_SPLITCACHE_GSE.log_status()
    DVBS2_STDLEN_SPLITCACHE_GSE.done_processing()
    DVBS2_STDLEN_STDCACHE_GSE.log_status()
    DVBS2_STDLEN_STDCACHE_GSE.done_processing()
    DVBS2_LEN2_SPLITCACHE_GSE.log_status()
    DVBS2_LEN2_SPLITCACHE_GSE.done_processing()
    DVBS2_LEN2_STDCACHE_GSE.log_status()
    DVBS2_LEN2_STDCACHE_GSE.done_processing()
    
    DVBS2_REV.log_status()
    DVBS2_REV.done_processing()
    

    # runs after the dvbs2 rev parser
    DVBS2_REV_IP.process_capture_file(DVBS2_REV.protocol_file, PREVIEW_LENGTH)
    DVBS2_REV_IP.log_status()
    DVBS2_REV_IP.done_processing()
    
    # runs after the dvbs2 gse parsers
    
    DVBS2_STDLEN_SPLITCACHE_GSE_IP.process_capture_file(DVBS2_STDLEN_SPLITCACHE_GSE.protocol_file, PREVIEW_LENGTH)
    DVBS2_STDLEN_SPLITCACHE_GSE_IP.log_status()
    DVBS2_STDLEN_SPLITCACHE_GSE_IP.done_processing()
    
    DVBS2_STDLEN_STDCACHE_GSE_IP.process_capture_file(DVBS2_STDLEN_STDCACHE_GSE.protocol_file, PREVIEW_LENGTH)
    DVBS2_STDLEN_STDCACHE_GSE_IP.log_status()
    DVBS2_STDLEN_STDCACHE_GSE_IP.done_processing()

    DVBS2_LEN2_SPLITCACHE_GSE_IP.process_capture_file(DVBS2_LEN2_SPLITCACHE_GSE.protocol_file, PREVIEW_LENGTH)
    DVBS2_LEN2_SPLITCACHE_GSE_IP.log_status()
    DVBS2_LEN2_SPLITCACHE_GSE_IP.done_processing()

    DVBS2_LEN2_STDCACHE_GSE_IP.process_capture_file(DVBS2_LEN2_STDCACHE_GSE_IP.protocol_file, PREVIEW_LENGTH)
    DVBS2_LEN2_STDCACHE_GSE_IP.log_status()
    DVBS2_LEN2_STDCACHE_GSE_IP.done_processing()
    
    # DVBS2_LEN2_SPLITCACHE_GSE_MPEGTS.process_capture_file(DVBS2_LEN2_SPLITCACHE_GSE.protocol_file, PREVIEW_LENGTH)
    # DVBS2_LEN2_SPLITCACHE_GSE_MPEGTS.log_status()
    # DVBS2_LEN2_SPLITCACHE_GSE_MPEGTS.done_processing()
    
    first_pass = {
        "[DVBS2]": DVBS2,
        "[MPEGTS]": MPEGTS,
        "[IP]": IP
    }

    second_pass = {
        "[DVBS2] -> [CRC MPEGTS]": DVBS2_CRC_MPEGTS,
        "[DVBS2] -> [NEWTEC CRC]": DVBS2_NEWTEC_CRC,   
        "[DVBS2] -> [STDLEN 6/2 GSE]": DVBS2_STDLEN_SPLITCACHE_GSE,
        "[DVBS2] -> [STDLEN STD GSE]": DVBS2_STDLEN_STDCACHE_GSE,
        "[DVBS2] -> [LEN-2 6/2 GSE]": DVBS2_LEN2_SPLITCACHE_GSE,
        "[DVBS2] -> [LEN-2 STD GSE]": DVBS2_LEN2_STDCACHE_GSE,
        "[DVBS2] -> [MPEGTS]": DVBS2_MPEGTS,
        "[DVBS2] -> [IP]": DVBS2_IP,
        "[DVBS2] -> [REV] -> [IP]": DVBS2_REV_IP
    }

    third_pass = {
        "[DVBS2] -> [STDLEN 6/2 GSE] -> [IP]": DVBS2_STDLEN_SPLITCACHE_GSE_IP,
        "[DVBS2] -> [IP]": DVBS2_IP,
        "[DVBS2] -> [STDLEN STD GSE] -> [IP]": DVBS2_STDLEN_STDCACHE_GSE_IP,
        "[DVBS2] -> [LEN-2 6/2 GSE] -> [IP]": DVBS2_LEN2_SPLITCACHE_GSE_IP,
        "[DVBS2] -> [LEN-2 STD GSE] -> [IP]": DVBS2_LEN2_STDCACHE_GSE_IP,
        "[DVBS2] -> [REV] -> [IP]": DVBS2_REV_IP,
        # "[DVBS2] -> [LEN2 6/2 GSE] -> [MPEGTS]": DVBS2_LEN2_SPLITCACHE_GSE_MPEGTS
    }

    # --- Round One ---
    first_pass_sort = sorted(first_pass.items(), key=lambda kv: kv[1].get_compliance(), reverse=True)

    print(f"\nROUND ONE, Winner is {first_pass_sort[0][1].protocol_file}")
    for i, (name, obj) in enumerate(first_pass_sort, start=1):
        print(f"Rank {i}: {name} with score {obj.get_compliance():.2f}")

    # --- Round Two ---
    dvbs2_rankings = sorted(second_pass.items(), key=lambda kv: kv[1].get_compliance(), reverse=True)

    if isinstance(first_pass_sort[0][1], DVBS2Parser):
        print(f"\nROUND TWO, Winner is {dvbs2_rankings[0][1].protocol_file}")
        for i, (name, obj) in enumerate(dvbs2_rankings, start=1):
            print(f"Rank {i}: {name} with score {obj.get_compliance():.2f}")

    # --- Round Three ---
    ip_rankings = sorted(third_pass.items(), key=lambda kv: kv[1].get_compliance(), reverse=True)

    if isinstance(first_pass_sort[0][1], DVBS2Parser) and (isinstance(dvbs2_rankings[0][1], Len2SplitCacheGSEParser) \
            or isinstance(dvbs2_rankings[0][1], StandardLenSplitCacheGSEParser)\
            or isinstance(dvbs2_rankings[0][1], StandardLenStandardCacheGSEParser)\
            or isinstance(dvbs2_rankings[0][1], Len2StandardCacheGSEParser)):
        print(f"\nROUND THREE, Winner is {ip_rankings[0][1].protocol_file}")
        for i, (name, obj) in enumerate(ip_rankings, start=1):
            print(f"Rank {i}: {name} with score {obj.get_compliance():.2f}")


    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()