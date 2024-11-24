import os

def list_of_files(folder):
    try:
        files = os.listdir(folder)
        return files
    except FileNotFoundError:
        return folder,"Invalid path"
    
def list_files(files):
     for file in files:
        print(file)
        return file

def main():
    folder_path = input("Please enter the folder paths").split()
    for folder in folder_path:
        files = list_of_files(folder)
        #fsize = size_files(file)
        print("below are the files in the folder",folder)
        file = list_files(files)
        try:
            fsize = os.path.getsize(file)
            print(fsize)
        except FileNotFoundError:
                    print("No such file or directory")
        continue
        print(fsize)

if __name__ == "__main__":
    main()