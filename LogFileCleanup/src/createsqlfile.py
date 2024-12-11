import os
import shutil
import configparser
from datetime import datetime
from log_utils import write_log

config = configparser.ConfigParser()
config.read("Config.ini")

archive_dir = config.get("sql", "archive_dir")

def create_sql_file(archived_files_data, archived_files_data_zip, sql_file_path):
    try:
 
        with open(sql_file_path, 'w') as sql_file:

            sql_file.write("CREATE TABLE archived_files (\n")
            sql_file.write("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
            sql_file.write("    file_name TEXT,\n")
            sql_file.write("    original_path TEXT,\n")
            sql_file.write("    new_path TEXT,\n")
            sql_file.write("    file_time_details TEXT,\n")
            sql_file.write("    object_name TEXT\n")
            sql_file.write(");\n\n")

            
            for file_data in archived_files_data:
                file_name = file_data['file_name']
                original_path = file_data['original_path']
                new_path = file_data['new_path']
                file_time_details = file_data['file_time_details'].strftime('%Y-%m-%d %H:%M:%S')
                for zip_file_data in archived_files_data_zip:
                    archived_file = zip_file_data['object_name']

                    sql_file.write(f"INSERT INTO archived_files (file_name, original_path, new_path, file_time_details, object_name) VALUES ")
                    sql_file.write(f"('{file_name}', '{original_path}', '{new_path}', '{file_time_details}', '{archived_file}');\n")


            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            archive_file_name = f"archived_files_{timestamp}.sql"
            archived_file_path = os.path.join(archive_dir, archive_file_name)

            shutil.move(sql_file_path, archived_file_path)
            write_log(f"SQL file '{sql_file_path}' successfully created.")
        return True
    except Exception as e:
        write_log(f"Failed to create SQL file: {e}")
        return False
