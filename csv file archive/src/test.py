import os
import zipfile
from datetime import datetime, timedelta
import configparser
import shutil
import glob
#from log_utils import write_log, setup_logging

config = configparser.ConfigParser()
config.read("config.ini")

source_directory = config.get("Paths", "source_directory", fallback="H:\\")
output_zip = config.get("Paths", "output_zip", fallback="archived_csv_files.zip")
zip_files = config.get('Paths', 'zip_file')
ExportedFiles = config.get("Paths", "ExportedFiles")
current_date = datetime.now()
cutoff_date = current_date - timedelta(days=15)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def archive_csv():

    #setup_logging()

    print("Starting the process to zip old CSV files.")

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (file.endswith(".csv")) and (file_mod_time <= cutoff_date):
                new_file_name = f"{timestamp}_{file}"
                destination_path = os.path.join(ExportedFiles, new_file_name)
                shutil.move(file_path, destination_path)
                print(f"File found and moving the file {file_path} to {ExportedFiles}")
            else:
                print(f"No CSV file found to archive")
    print("Archive Function completed.")
    #archive_log()
    zip(ExportedFiles, output_zip)
    #push_to_s3(zip_file, bucket_name, object_name)
    


def zip(ExportedFiles, output_zip):

    files_zipped = False
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ExportedFile in os.listdir(ExportedFiles):
                file_path = os.path.join(ExportedFiles, ExportedFile)
                #print(Exportedfile1)
                if (os.path.isfile(file_path)) and  (file_path.endswith(".csv")): 
                    zipf.write(file_path, arcname=ExportedFile)
                    files_zipped = True
                    for zips in os.listdir(zip_files):
                        if zips.endswith(".zip"):
                            print(f"{ExportedFile} is Zipped into {output_zip}.")
                        else:
                            print(f"No csv file found in {ExportedFiles} to zip")
                    try:
                        os.remove(file_path)
                        print(f"Deleted {ExportedFile} after zipping.")
                    except Exception as e:
                        print(f"Failed to delete {ExportedFile}: {e}")
                else:
                    print("No CSV file found to ZIP, Ignore the below message")
                    
        if not files_zipped:
            os.remove(output_zip)
            print("No csv file found to zip")
        else:
            print(f"All the 15 days old csv files added into {output_zip}")
        
    finally:
        print("Function zip completed")
    
if __name__ == "__main__":
    archive_csv()
