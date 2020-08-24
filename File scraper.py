# File scraper
# github.com/smcclennon

import os, glob
from shutil import copyfile

file_format = [".png", ".jpg", ".gif", ".jpeg"]  # filetypes to copy
save_dir = 'img'  # path to copy files to
search_dir = "C:/Users/shira/Pictures"  # directory to search for files
filelist = []


# files already grabbed
try:
    os.mkdir(save_dir)  # create save_dir
    print(f'Created directory: {save_dir}')
except:
    pass

print('Checking files which have already been copied...')
for file in glob.iglob(f'{save_dir}/**', recursive=True):
    filelist.append(os.path.basename(file))  # keep track of files which have already been copied


def filesavename(file):
    filename, file_extension = os.path.splitext(file)
    return os.path.basename(filename)+" ("+(os.path.dirname(file)).replace(":", ";", 1).replace('/', '¦').replace('\\', '¦')+")"+file_extension  # format the copied files filenames

# searching for files to be grabbed
print(f'Searching recursively in: {search_dir}')
for file in glob.iglob(f'{search_dir}/**', recursive=True):
    if filesavename(file) not in filelist:  # if not duplicate (already copied)
        for value in file_format:
            if file.endswith(value):
                print(f'Copying: {file}')
                copyfile(file, f"{save_dir}/"+filesavename(file))
input('Done! Press enter to exit')