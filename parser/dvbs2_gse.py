import logging
import os
import argparse

from parser.config import plot_dir, write_dir, logs_dir, promising_dir
from parser.config import HEADER_LEVEL_NUM, PAYLOAD_LEVEL_NUM, PREVIEW_LENGTH

from parser.parsers.dvbs2.dvbs2_parser import DVBS2Parser
from parser.parsers.gse.gse_parser import StandardLenSplitCacheGSEParser, StandardLenStandardCacheGSEParser, Len2SplitCacheGSEParser, Len2StandardCacheGSEParser

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

    DVBS2.add_parser(GSE_INSTANCE)
    DVBS2.process_capture_file(capture_file)
    DVBS2.log_status()
    DVBS2.done_processing()
    
    GSE_INSTANCE.log_status()
    GSE_INSTANCE.done_processing()
    
    

    
    # STDLEN_SPLITCACHE_GSE = StandardLenSplitCacheGSEParser(DVBS2.protocol_file, protocol='stdlen.split.gse', log_level=log_level)
    # STDLEN_STDCACHE_GSE = StandardLenStandardCacheGSEParser(DVBS2.protocol_file, protocol='stdlen.std.gse', log_level=log_level)
    # LEN2_SPLITCACHE_GSE = Len2SplitCacheGSEParser(DVBS2.protocol_file, protocol='len2.split.gse', log_level=log_level)
    # LEN2_STDCACHE_GSE = Len2StandardCacheGSEParser(DVBS2.protocol_file, protocol='len2.std.gse', log_level=log_level)

    
    # DVBS2.add_parser(STDLEN_SPLITCACHE_GSE)
    # DVBS2.add_parser(STDLEN_STDCACHE_GSE)
    # DVBS2.add_parser(LEN2_SPLITCACHE_GSE)
    # DVBS2.add_parser(LEN2_STDCACHE_GSE)
    
    # DVBS2.process_capture_file(capture_file, PREVIEW_LENGTH)
    # DVBS2.log_status()
    # DVBS2.done_processing()
    
    # STDLEN_SPLITCACHE_GSE.log_status()
    # STDLEN_SPLITCACHE_GSE.done_processing()
    # STDLEN_STDCACHE_GSE.log_status()
    # STDLEN_STDCACHE_GSE.done_processing()
    # LEN2_SPLITCACHE_GSE.log_status()
    # LEN2_SPLITCACHE_GSE.done_processing()
    # LEN2_STDCACHE_GSE.log_status()
    # LEN2_STDCACHE_GSE.done_processing()

    # if DVBS2.get_compliance() > .90:
    #     if STDLEN_SPLITCACHE_GSE.bytes_skipped > LEN2_SPLITCACHE_GSE.bytes_skipped:
    #         # print("hdrlen-2")
    #         if LEN2_SPLITCACHE_GSE.split_fragment_cache.num_reassembled > LEN2_STDCACHE_GSE.fragment_cache.num_reassembled:
    #             print("hdrlen-2 and 6/2 frag_id/counter gse")
    #             os.system(f"mv '{LEN2_SPLITCACHE_GSE.protocol_file}' {promising_dir}")
    #         else: 
    #             print("hdrlen-2 and standard frag_id gse")
    #             os.system(f"mv '{LEN2_STDCACHE_GSE.protocol_file}' {promising_dir}")
    #     else: 
    #         # print("standard length")
    #         if STDLEN_SPLITCACHE_GSE.split_fragment_cache.num_reassembled > LEN2_STDCACHE_GSE.fragment_cache.num_reassembled:
    #             print("standard length and 6/2 frag_id/counter gse")
    #             os.system(f"mv '{STDLEN_SPLITCACHE_GSE.protocol_file}' {promising_dir}")
    #         else:
    #             print("standard length and standard frag_id gse")
    #             os.system(f"mv '{STDLEN_STDCACHE_GSE.protocol_file}' {promising_dir}")

    
    

    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()