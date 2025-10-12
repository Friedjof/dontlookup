import logging
import os
import argparse
from tqdm import tqdm 

from parser.config import plot_dir, write_dir, logs_dir
from parser.config import HEADER_LEVEL_NUM, PAYLOAD_LEVEL_NUM

from parser.utils.parser_utils import ParserBase

from todo import Todo

class TodoParser(ParserBase):
    def __init__(self, read_file, show_pbar=False, log_level=logging.INFO):
        super().__init__(read_file, protocol='todo', show_pbar=show_pbar, log_level=log_level)
        # add custom variables here
        pass
    def is_todo(self, byte_window):
        try:
            todo_packet = Todo.from_bytes(byte_window)
        except Exception as e:
            self.logger.error(f"Error parsing Todo: {e}", exc_info=True)
            pass
        else:
            return todo_packet
    def process_capture(self, capture):
        # TODO for user to implement
        pass
    def process_capture_file(self, capture_file, preview_len=None):
        super().process_capture_file(capture_file, preview_len)
    def done_processing(self):
        super().done_processing()
    def log_status(self, logger=None):
        super().log_status(self.logger)    
        logger = self.logger if logger == None else logger
        # TODO log custom performance metrics here


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
    
    todo = TodoParser(capture_file, log_level=log_level)
    todo.process_capture_file(capture_file)
    todo.log_status()
    todo.done_processing()

    logging.shutdown() # Ensures all log handlers are properly flushed and closed

if __name__ == "__main__":
    main()