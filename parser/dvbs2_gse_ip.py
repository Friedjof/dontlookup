import logging
import os
import argparse

from parser.config import plot_dir, write_dir, logs_dir, promising_dir
from parser.config import HEADER_LEVEL_NUM, PAYLOAD_LEVEL_NUM, PREVIEW_LENGTH

from parser.parsers.dvbs2.dvbs2_parser import DVBS2Parser
from parser.parsers.gse.gse_parser import StandardLenSplitCacheGSEParser, StandardLenStandardCacheGSEParser, Len2SplitCacheGSEParser, Len2StandardCacheGSEParser
from parser.parsers.ip.ip_parser import IPv4Parser

def main():
    parser = argparse.ArgumentParser(description="Process DVBS2 capture files with custom logging verbosity.")
    parser.add_argument("capture_file", help="Path to the input raw capture file.")
    parser.add_argument(
        "--parser",
        required=True,
        choices=[
            "stdlen.split",
            "stdlen.std",
            "len2.split",
            "len2.std",
        ],
        help="Choose which parser to run",
    )
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

    parser_map = {
        "stdlen.split": StandardLenSplitCacheGSEParser,
        "stdlen.std": StandardLenStandardCacheGSEParser,
        "len2.split": Len2SplitCacheGSEParser,
        "len2.std": Len2StandardCacheGSEParser,
    }

    capture_file = args.capture_file
    ParserClass = parser_map[args.parser]

    DVBS2 = DVBS2Parser(capture_file, log_level=log_level, show_pbar=True)
    
    GSE_INSTANCE = ParserClass(
        DVBS2.protocol_file,
        protocol=f"{args.parser}.gse",  # still pass full protocol name
        log_level=log_level
    )

    IP = IPv4Parser(GSE_INSTANCE.protocol_file, show_pbar=True, log_level=log_level)
    
    DVBS2.add_parser(GSE_INSTANCE)
    DVBS2.process_capture_file(capture_file)
    DVBS2.log_status()
    DVBS2.done_processing()
    
    GSE_INSTANCE.log_status()
    GSE_INSTANCE.done_processing()
    
    IP.process_capture_file(GSE_INSTANCE.protocol_file)
    IP.log_status()
    IP.done_processing()
    
    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()