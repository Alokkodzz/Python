import os
import shutil
import logging
from configparser import ConfigParser
from datetime import datetime

config = ConfigParser()
config.read('Config.ini')
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_file1 = config.get('Paths', 'log_file')
#log_file1 ="E:/Alok_AWS/Devops_Notes/Python/sql/logs/logfile_{timestamp}.log"
log_file = log_file1.format(timestamp=timestamp)
log_file_path = config.get("Paths", "log_file_path")
#log_file_path = "E:/Alok_AWS/Devops_Notes/Python/sql/logs/"
archive_folder_path = config.get('Paths', 'archive_folder')
#archive_folder_path = "E:/Alok_AWS/Devops_Notes/Python/sql/logs/archives/"



def setup_logging():
# Read configuration

# Get the log file and archive folder path from the config
#log_file_path = config.get('Paths', 'log_file_path')
#archive_folder_path = config.get('Paths', 'archive_folder')

# Set up logging to the log file
    
    logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def write_log(message):
# Write a log message
    logging.info(message)

def archive_log():
    # Read configuration
    config = ConfigParser()
    config.read('config.ini')

    # Get the log file and archive folder path from the config
    '''log_file1 = config.get('Paths', 'log_file')
    log_files = log_file1.format(timestamp=timestamp)
    log_file_path = config.get("Paths", "log_file_path")
    archive_folder_path = config.get('Paths', 'archive_folder')'''

    #with open(log_file_path, "w") as log_file:

    # Check if the archive folder exists
    
    archive_log_path = os.path.join(archive_folder_path, f"logfile_{timestamp}.log")
    for file in os.listdir(log_file_path):
        file_path = os.path.join(log_file_path, file)
        if os.path.isfile(file_path) and not file.endswith(f"logfile_{timestamp}.log"):

            try:
                # Move the log file to the archive folder
                shutil.move(file_path, archive_log_path)
                print(f"Log file moved to archive: {archive_log_path}")
                #archive_log_path.close(archive_folder_path)
            except Exception as e:
                print(f"Error moving log file: {e}")
        else:
            print(f"Archive folder does not exist: {archive_folder_path}")
