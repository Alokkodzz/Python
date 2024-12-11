import os
import boto3
import shutil
import zipfile
from datetime import datetime, timedelta
import configparser
from log_utils import setup_logging, write_log, archive_log
from smtp import send_email_success, send_email_failed
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from createsqlfile import create_sql_file


config = configparser.ConfigParser()
config.read("Config.ini")

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


#Variables for the function archive_log
source_directory = config.get("Paths", "source_directory", fallback="H:\\")
output_zip = config.get("Paths", "output_zip", fallback="archived_log_files.zip")
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

#constant for sql file
sql_file_path = config.get("sql", "sql_file_path")
archived_files_data = []
archived_files_data_zip = []

def archive_log_files():

    setup_logging()

    counter = 1

    write_log("Starting the process to zip old log files.")

    for root, dirs, files in os.walk(source_directory):
        for file in files:
            file = file
            file_path = os.path.join(root, file)
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if (file.endswith(".log")) and (file_mod_time <= cutoff_date):
                new_file_name = f"{counter}_{file}"
                destination_path = os.path.join(ExportedFiles, new_file_name)
                shutil.move(file_path, destination_path)
                #shutil.move(file_path, ExportedFiles)
                write_log(f"File found and moving the file {file_path} to temp location")
                counter += 1

                archived_files_data.append({'file_name' : file, 
                                          'original_path' : file_path, 
                                          'new_path' : ExportedFiles,
                                          'file_time_details' : file_mod_time
                                          })

    write_log("Archive Function completed.")
    archive_log()
    #listoffiles = os.listdir(ExportedFiles)
    #write_log(f"{listoffiles}")
    zip(ExportedFiles, output_zip)


def zip(ExportedFiles, output_zip):

    files_zipped = False
    try:
        with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for ExportedFile in os.listdir(ExportedFiles):
                file_path = os.path.join(ExportedFiles, ExportedFile)
                #write_log(Exportedfile1)
                if (os.path.isfile(file_path)) and  (file_path.endswith(".log")): 
                    zipf.write(file_path, arcname=ExportedFile)
                    files_zipped = True
                    for zips in os.listdir(zip_files):
                        if zips.endswith(".zip"):
                            write_log(f"'{ExportedFile}' is Zipped into '{object_name}'.")
                        else:
                            write_log(f"No log file found in {ExportedFiles} to zip")
                    try:
                        os.remove(file_path)
                        write_log(f"Deleted {ExportedFile} after zipping.")
                    except Exception as e:
                        write_log(f"Failed to delete {ExportedFile}: {e}")
                else:
                    write_log("No log file found to ZIP, Ignore the below message")
                    
        if not files_zipped:
            os.remove(output_zip)
            write_log("No log file found to zip")
        else:
            write_log(f"All the 15 days old log files added into {object_name}")
            archived_files_data_zip.append({'object_name' : object_name})
            create_sql_file(archived_files_data, archived_files_data_zip, sql_file_path)
        
    finally:
        write_log("Function zip completed")
        push_to_s3(zip_file, bucket_name, object_name, region_name=region)

def push_to_s3(zip_file, bucket_name, object_name=None, region_name="us-east-1"):

    client = boto3.client("s3", region_name=region_name)


    # Use the file name if no object name is provided
    if object_name is None:
        object_name = zip_file.split("/")[-1]

    #archived_files_data.append({'archive_file' : object_name})
    
    #write_log(archived_files_data)
    


    try:
        # Upload the file
        client.upload_file(zip_file, bucket_name, object_name)
        write_log(f"File '{object_name}' successfully uploaded to bucket : {bucket_name}.")
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
    archive_log_files()
    #zip(ExportedFiles, output_zip)