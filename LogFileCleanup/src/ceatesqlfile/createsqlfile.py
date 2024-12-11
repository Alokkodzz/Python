from log_utils import write_log

def create_sql_file(archived_files_data, sql_file_path):
    try:
        # Create the SQL file
        with open(sql_file_path, 'w') as sql_file:
            # SQL table creation statement
            sql_file.write("CREATE TABLE archived_files (\n")
            sql_file.write("    id INTEGER PRIMARY KEY AUTOINCREMENT,\n")
            sql_file.write("    file_name TEXT,\n")
            sql_file.write("    original_path TEXT,\n")
            sql_file.write("    new_path TEXT,\n")
            sql_file.write("    file_time_details TEXT\n")
            sql_file.write("    archive_file TEXT\n")
            sql_file.write(");\n\n")
            
            # Insert data for each archived file
            for file_data in archived_files_data:
                file_name = file_data['file_name']
                original_path = file_data['original_path']
                new_path = file_data['new_path']
                file_time_details = file_data['file_time_details'].strftime('%Y-%m-%d %H:%M:%S')
                archive_file = file_data['archive_file']
                
                # SQL insert statement for each file
                sql_file.write(f"INSERT INTO archived_files (file_name, original_path, new_path, file_time_details) VALUES ")
                sql_file.write(f"('{file_name}', '{original_path}', '{new_path}', '{file_time_details}', '{archive_file}');\n")

        write_log(f"SQL file '{sql_file_path}' successfully created.")
        return True
    except Exception as e:
        write_log(f"Failed to create SQL file: {e}")
        return False
