# File scraper
# github.com/smcclennon

import os, glob, time
from shutil import copyfile


type_blacklist = [".mp4", ".mov", ".gif"]  # filetypes to ignore
save_dir = 'directory/subdirectory'  # path to copy files to
search_dir = [r"C:\Users\shira\Documents\GitHub\smcclennon.github.io\assets\css",  # directory to search for files
               r"C:\Users\shira\Documents\GitHub\smcclennon.github.io\assets\js"
               ]
filelist = []
old_files = 0
new_files = 0
new_dirs = 0
skipped_files = 0
errors = 0

def filesavename(file):
    filename, file_extension = os.path.splitext(file)
    return (os.path.dirname(file)[2:]).replace("\\", "/")+"/"+os.path.basename(filename)+file_extension  # format the copied files filenames, [2:] removes C:

try:
    if not os.path.exists(save_dir):
         os.makedirs(save_dir)  # create save_dir
    print(f'Created directory: {save_dir}')
except Exception as e:
    print(e)
    input('Press enter to continue')

print('[ SCAN ] Checking pre-existing files', end="")
for file in glob.iglob(f"{save_dir}/**", recursive=True):
    if os.path.isfile(file):
        filelist.append(filesavename(file.replace(save_dir, 'X:', 1)))  # keep track of files which have already been copied
        print(".", end="")


start = time.time()
# searching for files to be grabbed
for directory in search_dir:
    print(f'\n[ COPY ] Copying files from: {directory}', end='')
    for file in glob.iglob(f"{directory}/**", recursive=True):  # Find all files and folders
        if os.path.isfile(file):
            for value in type_blacklist:
                if file.endswith(value):
                    print(f'\n[ SKIP ] {value}: {file}', end='')
                    skipped_files += 1
                else:
                    if filesavename(file) not in filelist:  # if not duplicate (already copied)
                        print('.', end='')
                        new_files += 1
                    else:
                        print('.', end='')
                        old_files += 1
                    new_dir = os.path.dirname(save_dir+filesavename(file)).replace("/","\\")
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)  # create save_dir
                        print(':', end='')
                        new_dirs += 1
                    try:
                        copyfile(file, save_dir+filesavename(file))
                    except Exception as e:
                            print(f"[ ERROR ] {e}")
                            errors += 1
finish = time.time()
print(f'''\n\n
New files: {new_files}
Replaced files: {old_files}
Directories created: {new_dirs}
''')
input(f'Processed {old_files+new_files} files in {round(finish-start, 2)} seconds with {errors} errors!')
