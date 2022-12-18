import os
import shutil
import threading
from concurrent.futures import ThreadPoolExecutor
import time


def log_thread_and_time(func):
    def wrapper(*args, **kwargs):
        '''Get the current number of threads'''
        num_threads = threading.active_count()

        '''Record the start time'''
        start_time = time.perf_counter()

        '''Call the function'''
        result = func(*args, **kwargs)

        '''Record the end time'''
        end_time = time.perf_counter()

        '''Calculate the elapsed time'''
        elapsed_time = end_time - start_time

        '''Log the number of threads, elapsed time, and quantity of files moved'''
        print(
            f"Number of threads: {num_threads}, elapsed time = {elapsed_time:.2f}s, files moved = {result}")
    return wrapper


def normalize(string: str):
    '''Define a string containing all cyrillic symbols and a corresponding translation list'''
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    '''Create an empty list to store the normalized characters'''
    lst = []

    '''Create a translation dictionary using the cyrillic symbols and their corresponding translations'''
    trans = {}
    for c, l in zip(cyrillic_symbols, translation):
        trans[ord(c)] = l
        trans[ord(c.upper())] = l.upper()

    '''Iterate through each character in the input string'''
    for i in string:
        '''If the character is alphanumeric, append it to the list as is'''
        if i in "0123456789" or ord(i) in range(65, 91) or ord(i) in range(97, 123):
            lst.append(i)

            '''If the character is a cyrillic symbol, translate it to its corresponding latin character and append it to the list'''
        elif i in cyrillic_symbols:
            lst.append(i.translate(trans))

            '''If the character is an uppercase letter, translate it to its corresponding latin character (if it is a cyrillic symbol)'''
            '''or append an underscore to the list (if it is not a cyrillic symbol)'''

        elif i.isupper():
            if i.lower() in cyrillic_symbols:
                lst.append(i.lower().translate(trans).upper())
            else:
                lst.append("_")

            '''Else the character is any other non-alphanumeric character, append an underscore to the list'''
        else:
            lst.append("_")

    '''Join the normalized characters in the list into a single string and return it'''
    new_string = "".join(lst)
    return new_string


@log_thread_and_time
def sorting(path: str):
    '''Create a counter to track the number of files processed'''
    num_files_processed = 0
    '''Create a dictionary to store the files by extension'''
    files_by_extension = {}

    '''Map file extensions to destination folders'''
    extension_map = {
        extension: folder
        for extensions, folder in [
            (('.AVI', '.MP4', '.MOV', '.MKV'), 'video'),
            (('.BMP', '.JPEG', '.PNG', '.JPG', '.SVG', 'GIF'), 'images'),
            (('.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.XLSM'), 'documents'),
            (('.MP3', '.WAV', '.WMA'), 'audio'),
            (('.ZIP', '.RAR', '.APK'), 'archives')
        ]
        for extension in extensions
    }

    '''Process the current directory'''
    '''Sort the files in the current directory by extension'''
    for file in os.listdir(path):
        '''Get the extension of the file'''
        extension = os.path.splitext(file)[1]

        '''Add the file to the dictionary using the extension as the key'''
        if extension in files_by_extension:
            files_by_extension[extension].append(file)
        else:
            files_by_extension[extension] = [file]

    '''Process each subdirectory using a thread pool'''
    with ThreadPoolExecutor(max_workers=10) as executor:
        '''Create a list of tuples containing the subdirectory and the normalized name'''
        subdirectories = [(subdirectory, normalize(subdirectory)) for
                          subdirectory in os.listdir(path) if os.path.isdir(os.path.join(path, subdirectory))]

        '''Process each subdirectory in a separate thread'''
        for subdirectory, normalized_name in subdirectories:
            '''Create the destination path for the subdirectory'''
            destination_path = os.path.join(path, normalized_name)

            '''Create the destination folder if it does not exist'''
            if not os.path.exists(destination_path):
                os.makedirs(destination_path)

            '''Submit the task to the thread pool'''
            executor.submit(sorting, os.path.join(path, subdirectory))

    '''Process the files in the current directory'''
    for extension, files in files_by_extension.items():
        '''Get the destination folder for the extension'''
        destination_folder = extension_map.get(extension.upper(), 'other')

        '''Create the destination path for the files'''
        destination_path = os.path.join(path, destination_folder)

        '''Create the destination folder if it does not exist'''
        if not os.path.exists(destination_path):
            os.makedirs(destination_path)

        '''Move each file to the destination folder'''
        for file in files:
            '''Get the source and destination paths for the file'''
            source_path = os.path.join(path, file)
            destination_path = os.path.join(path, destination_folder, file)

            '''Move the file'''
            shutil.move(source_path, destination_path)

            '''Increment the counter'''
            num_files_processed += 1

    '''Return the number of files processed'''
    return num_files_processed


def main():
    '''Prompt the user for the path to the folder that they want to sort'''

    path = input('Enter path to folder which should be cleaned:')
    if not (os.path.exists(path) and os.path.isdir(path)):
        print('Path incorrect. Try again')
        main()
        
    '''Sort the files in the specified folder'''
    sorting(path)
    print("Everything done. Please cross check")


if __name__ == '__main__':
    main()
