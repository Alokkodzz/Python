import os
import shutil
import zipfile
import boto3
from datetime import datetime, timedelta
import configparser
from log_utils import setup_logging, write_log, archive_log
from smtp import send_email_success, send_email_failed

config = configparser.ConfigParser()
config.read("config.ini")

# AWS DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name=config.get("ses", "aws_region"))
table = dynamodb.Table('archived_files')  # Use the DynamoDB table name

# Variables and configurations from config.ini
source_directory = config.get("Paths", "source_directory", fallback="H:\\")
ExportedFiles = config.get("Paths", "ExportedFiles")
output_zip = config.get("Paths", "output_zip", fallback="archived_csv_files.zip")
cutoff_date = datetime.now() - timedelta(days=15)

# Function to insert file metadata into DynamoDB
def insert_file_record_to_dynamodb(file_name, file_path, zip_file, status="Archived"):
    try:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
        file_id = f"{file_name}_{timestamp}"  # Unique ID based on file name and timestamp

        response = table.put_item(
            Item={
                'file_id': file_id,  # Partition key
                'file_name': file_name,
                'file_path': file_path,
                'zip_file': zip_file,
                'archived_on': timestamp,
                'status': status
            }
        )
        write_log(f"Inserted {file_name} into DynamoDB with status {status}.")
    except Exception as e:
        write_log(f"Error inserting record into DynamoDB: {e}")

def archive_csv():
    setup_logging()
    counter = 1
    write_log("Starting the process to zip old CSV files.")

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if file.endswith(".csv") and file_mod_time <= cutoff_date:
                new_file_name = f"{counter}_{file}"
                destination_path = os.path.join(ExportedFiles, new_file_name)
                shutil.move(file_path, destination_path)
                write_log(f"File found and moving the file {file_path} to {ExportedFiles}")
                # Insert the record into DynamoDB
                insert_file_record_to_dynamodb(file, file_path, output_zip)
                counter += 1

    write_log("Archive Function completed.")
    archive_log()
    zip(ExportedFiles, output_zip)

def zip(ExportedFiles, output_zip):
    files_zipped = False
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ExportedFile in os.listdir(ExportedFiles):
                file_path = os.path.join(ExportedFiles, ExportedFile)
                if os.path.isfile(file_path) and file_path.endswith(".csv"):
                    zipf.write(file_path, arcname=ExportedFile)
                    files_zipped = True
                    write_log(f"{ExportedFile} is Zipped into {output_zip}.")
                    try:
                        os.remove(file_path)
                        write_log(f"Deleted {ExportedFile} after zipping.")
                    except Exception as e:
                        write_log(f"Failed to delete {ExportedFile}: {e}")
        
        if not files_zipped:
            os.remove(output_zip)
            write_log("No CSV file found to zip.")
        else:
            write_log(f"All the 15 days old CSV files added into {output_zip}")
        
    finally:
        write_log("Function zip completed")

if __name__ == "__main__":
    archive_csv()
