CREATE TABLE archived_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT,
    original_path TEXT,
    new_path TEXT,
    file_time_details TEXT,
    object_name TEXT,
);

INSERT INTO archived_files (file_name, original_path, new_path, file_time_details) VALUES ('alok.log', 'H:\\test\alok.log', 'E:/Alok_AWS/Devops_Notes/Python/sql/ExportedFiles/', '2023-11-22 10:00:00', 'archived_log_files_2024-12-11_12-15-38.zip');
INSERT INTO archived_files (file_name, original_path, new_path, file_time_details) VALUES ('file.log', 'H:\\test\file.log', 'E:/Alok_AWS/Devops_Notes/Python/sql/ExportedFiles/', '2023-11-22 10:00:00', 'archived_log_files_2024-12-11_12-15-38.zip');
INSERT INTO archived_files (file_name, original_path, new_path, file_time_details) VALUES ('file2.log', 'H:\\test\file2.log', 'E:/Alok_AWS/Devops_Notes/Python/sql/ExportedFiles/', '2023-11-22 10:00:00', 'archived_log_files_2024-12-11_12-15-38.zip');
INSERT INTO archived_files (file_name, original_path, new_path, file_time_details) VALUES ('file3.log', 'H:\\test\file3.log', 'E:/Alok_AWS/Devops_Notes/Python/sql/ExportedFiles/', '2023-11-22 10:00:00', 'archived_log_files_2024-12-11_12-15-38.zip');
INSERT INTO archived_files (file_name, original_path, new_path, file_time_details) VALUES ('file4.log', 'H:\\test\file4.log', 'E:/Alok_AWS/Devops_Notes/Python/sql/ExportedFiles/', '2023-11-22 10:00:00', 'archived_log_files_2024-12-11_12-15-38.zip');
