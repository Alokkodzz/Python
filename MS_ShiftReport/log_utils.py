import logging
import configparser
from datetime import datetime
import pytz
import os, shutil

config = configparser.ConfigParser()
config.read("Config.ini")

utc_now = datetime.now(pytz.utc)
ist_timezone = pytz.timezone('Asia/Kolkata')
ist_now = utc_now.astimezone(ist_timezone)

timestamp = ist_now.strftime("%Y-%m-%d_%H-%M-%S")

log_file1 = config.get("Log", "log_file")
log_file = log_file1.format(datestamp=timestamp)

def setup_logging():
    
    logging.basicConfig(filename=log_file, level=logging.INFO,
                        format='%(asctime)s - %(message)s')
    

def write_log(message):
    logging.info(message)

def archive_log():

    archive_dirs = config.get("Log", "archive_dir")
    #if not os.path.exists(archive_dir):
     #           os.makedirs(archive_dir)

    archive_file_name = f"log_{timestamp}.log"
    archived_file_path = os.path.join(archive_dirs, archive_file_name)
    log_files = config.get("Log", "log_file_path")

    for file in os.listdir(log_files):
        file_path = os.path.join(log_files, file)
        if os.path.isfile(file_path) and not file.endswith(f"logfile_{timestamp}.log"):
            try:
                shutil.move(file_path, archived_file_path)

            except Exception as e:
                print(f"Error moving log file: {e}")

