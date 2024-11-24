import os
import boto3
import shutil
import zipfile
from datetime import datetime, timedelta
import configparser
from log_utils import setup_logging, write_log, archive_log
from smtp import send_email_success, send_email_failed
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


config = configparser.ConfigParser()
config.read("config.ini")

#aws keys
access_key = config.get("ses", "aws_access_key")
secret_key = config.get("ses", "aws_secret_key")
region = config.get("ses", "aws_region")

#Variables for the function push to s3
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
zip_file = config.get("s3", "zip_file")
bucket_name = config.get("s3", "bucket_name")
object_name_in_s3 = config.get("s3", "object_name")
object_name = object_name_in_s3.format(timestamp=timestamp)


#Variables for the function archive_csv
source_directory = config.get("Paths", "source_directory", fallback="H:\\")
output_zip = config.get("Paths", "output_zip", fallback="archived_csv_files.zip")
zip_files = config.get('Paths', 'zip_file')
ExportedFiles = config.get("Paths", "ExportedFiles")
current_date = datetime.now()
cutoff_date = current_date - timedelta(days=15)


#Variables for the function send emails
sender = config.get("Email", "sender")
recipient = config.get("Email", "recipient")
subject11 = config.get("Email", "subject1")
subject1 = subject11.format(timestamp=timestamp)
body_text11 = config.get("Email", "body_text1")
body_text1 = body_text11.format(timestamp=timestamp)
subject22 = config.get("Email", "subject2")
subject2 = subject22.format(timestamp=timestamp)
body_text22 = config.get("Email", "body_text2")
body_text2 = body_text22.format(timestamp=timestamp)

def archive_csv():

    setup_logging()

    counter = 1

    write_log("Starting the process to zip old CSV files.")

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (file.endswith(".csv")) and (file_mod_time <= cutoff_date):
                new_file_name = f"{counter}_{file}"
                destination_path = os.path.join(ExportedFiles, new_file_name)
                shutil.move(file_path, destination_path)
                #shutil.move(file_path, ExportedFiles)
                write_log(f"File found and moving the file {file_path} to {ExportedFiles}")
                counter += 1
            #else:
             #   write_log(f"No CSV file found to archive")
    write_log("Archive Function completed.")
    archive_log()
    listoffiles = os.listdir(ExportedFiles)
    write_log(f"{listoffiles}")
    zip(ExportedFiles, output_zip)
    push_to_s3(zip_file, bucket_name, object_name, region_name=region)
    


def zip(ExportedFiles, output_zip):

    files_zipped = False
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ExportedFile in os.listdir(ExportedFiles):
                file_path = os.path.join(ExportedFiles, ExportedFile)
                #write_log(Exportedfile1)
                if (os.path.isfile(file_path)) and  (file_path.endswith(".csv")): 
                    zipf.write(file_path, arcname=ExportedFile)
                    files_zipped = True
                    for zips in os.listdir(zip_files):
                        if zips.endswith(".zip"):
                            write_log(f"{ExportedFile} is Zipped into {output_zip}.")
                        else:
                            write_log(f"No csv file found in {ExportedFiles} to zip")
                    try:
                        os.remove(file_path)
                        write_log(f"Deleted {ExportedFile} after zipping.")
                    except Exception as e:
                        write_log(f"Failed to delete {ExportedFile}: {e}")
                else:
                    write_log("No CSV file found to ZIP, Ignore the below message")
                    
        if not files_zipped:
            os.remove(output_zip)
            write_log("No csv file found to zip")
        else:
            write_log(f"All the 15 days old csv files added into {output_zip}")
        
    finally:
        write_log("Function zip completed")

def push_to_s3(zip_file, bucket_name, object_name=None, region_name="us-east-1"):

    client = boto3.client("s3", region_name=region_name)

    # Use the file name if no object name is provided
    if object_name is None:
        object_name = zip_file.split("/")[-1]


    try:
        # Upload the file
        client.upload_file(zip_file, bucket_name, object_name)
        write_log(f"File '{zip_file}' successfully uploaded to '{bucket_name}/{object_name}'.")
        send_email_success(sender, recipient, subject1, body_text1, aws_region=region)
        write_log("Email sent!, Task completed")
        return True
    except FileNotFoundError:
        write_log(f" The file '{zip_file}' was not found.")
        send_email_failed(sender, recipient, subject2, body_text2, aws_region=region)
        write_log("Email sent!!!")
        return False
    except NoCredentialsError:
        write_log("Error: AWS credentials not available.")
        send_email_failed(sender, recipient, subject2, body_text2, aws_region=region)
        write_log("Email sent!!!")
        return False
    except PartialCredentialsError:
        write_log("Error: Incomplete AWS credentials configuration.")
        send_email_failed(sender, recipient, subject2, body_text2, aws_region=region)
        write_log("Email sent!!!")
        return False
    except Exception as e:
        write_log(f"Error : An error occurred: {e}")
        send_email_failed(sender, recipient, subject2, body_text2, aws_region=region)
        write_log("Email sent!!!")
        return False

if __name__ == "__main__":
    archive_csv()