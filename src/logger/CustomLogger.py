
import logging
import sys
import os

class CustomLogger(logging.getLoggerClass()):
     
    def __init__(self, name, log_dir=None):
        """This function initializes the CustomLogger class"""

        super().__init__(name)
        self.setLevel(logging.DEBUG)
        
        # Create stream handler for logging to stdout
        # self.stdout_handler = logging.StreamHandler(sys.stdout)
        # self.stdout_handler.setLevel(logging.DEBUG)
        # self.stdout_handler.setFormatter(logging.Formatter('%(message)s'))
        # self.addHandler(self.stdout_handler)
        
        # Add file handler only if the log directory was specified
        if log_dir:
            # Check if the log directory exists
            if not os.path.exists(os.path.dirname(log_dir)):
                os.makedirs(os.path.dirname(log_dir))
            self.add_file_handler(name, log_dir) 
    
    def add_file_handler(self, name, log_dir):
        self.file_handler = logging.FileHandler(log_dir,"w")
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.addHandler(self.file_handler)

    def get_path(self) -> str:
        return self.file_handler.baseFilename