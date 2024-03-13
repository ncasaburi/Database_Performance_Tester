import logging
import sys

class CustomLogger(logging.getLoggerClass()):
    
    def __init__(self, name, log_dir=None):
        super().__init__(name)
        self.setLevel(logging.DEBUG)
        
        # Create stream handler for logging to stdout
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setLevel(logging.DEBUG)
        self.stdout_handler.setFormatter(logging.Formatter('%(message)s'))
        self.addHandler(self.stdout_handler)
        
        # Add file handler only if the log directory was specified
        if log_dir:
            self.add_file_handler(name, log_dir)
    
    def add_file_handler(self, name, log_dir):
        file_handler = logging.FileHandler(log_dir,"w")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.addHandler(file_handler)