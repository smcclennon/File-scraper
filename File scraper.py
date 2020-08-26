# File scraper
# github.com/smcclennon

import os, glob, time, json
from shutil import copyfile

proj = "FileScraper"


config = {
    'type_blacklist': [".mp4", ".mov", ".gif"],
    'save_dir': 'directory/subdirectory',
    'search_dir': [
        "C:\\Users\\shira\\Pictures\\Screenshots",
        "C:\\FakeDirectory",
        "C:\\Users\\shira\Documents\\GitHub\\smcclennon.github.io\\assets\js"
    ]
}
try:
    with open(f"{proj}_config.json", "r") as config_file:
        config = json.load(config_file)
except:
    try:
        with open(f"{proj}_config.json", "w") as config_file:
            json.dump(config, config_file, sort_keys=True, indent=4)
            print(f'We couldn\'t find a config, so we\'ve created one ("{proj}_config.json").')
            print('You should edit this to your needs before continuing.')
            input('\nPress enter to exit...')
            exit()
    except Exception as e:
        print(e)
        input('Press enter to continue')



filelist = []
old_files = 0
new_files = 0
new_dirs = 0
skipped_files = 0
errors = 0
taskTimer = time.time()


def activePrint():
    global taskTimer
    if time.time() - taskTimer > 2:
        taskTimer = time.time()
        return "."
    else:
        return ""


def filesavename(file):
    filename, file_extension = os.path.splitext(file)
    return (os.path.dirname(file)[2:]).replace("\\", "/")+"/"+os.path.basename(filename)+file_extension  # format the copied files filenames, [2:] removes C:

try:
    if not os.path.exists(config["save_dir"]):
         os.makedirs(config["save_dir"])  # create save_dir
    print(f'Created save directory: {config["save_dir"]}')
except Exception as e:
    print(e)
    input('Press enter to continue')

print(f'[ SCAN ] Checking pre-existing files in the save directory... ', end="")
for file in glob.iglob(config["save_dir"]+"/**", recursive=True):
    if os.path.isfile(file):
        filelist.append(filesavename(file.replace(config["save_dir"], 'X:', 1)))  # keep track of files which have already been copied
        print(activePrint(), flush=True, end="")


start = time.time()
# searching for files to be grabbed
for directory in config["search_dir"]:
    print(f'\n[ COPY ] Copying files from: {directory}', end='')
    for file in glob.iglob(f"{directory}/**", recursive=True):  # Find all files and folders
        if os.path.isfile(file):
            for value in config["type_blacklist"]:
                if file.endswith(value):
                    print(f'\n[ SKIP ] {value}: {file}', end='')
                    skipped_files += 1
                else:
                    if filesavename(file) not in filelist:  # if not duplicate (already copied)
                        print(activePrint(), flush=True, end="")
                        new_files += 1
                    else:
                        print(activePrint(), flush=True, end="")
                        old_files += 1
                    new_dir = os.path.dirname(config["save_dir"]+filesavename(file)).replace("/","\\")
                    if not os.path.exists(new_dir):
                        os.makedirs(new_dir)  # create save_dir
                        print(activePrint(), flush=True, end="")
                        new_dirs += 1
                    try:
                        copyfile(file, config["save_dir"]+filesavename(file))
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
