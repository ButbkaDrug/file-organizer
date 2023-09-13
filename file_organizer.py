import os
import subprocess

HOME = os.getenv('HOME')
DOWNLOADS = os.path.join(HOME, 'Downloads')

content = os.listdir(DOWNLOADS)
threshold = 2

numbers = range(ord("1"), ord("9"))
letters = range(ord("A"), ord("z"))
extensions = {}
for file in content:
    if os.path.isdir(file):
        continue
    index = file.rfind(".")
    option = file[index+1:]
    if len(option) < 2 and option not in numbers and option not in letters:
        continue
    if option not in extensions:
        extensions.update({option:[file]})
    else:
        extensions[option].append(file)



print(f"Directory {DOWNLOADS}")
print(f"Total files: {len(content)}")
print(f"Total types: {len(extensions)}")

file_types = [x for x in extensions.items() if len(x[1]) > threshold]
dirs_to_create = [x[0] for x in file_types if not os.path.isdir(x[0])]
files_to_move = sum([len(x[1]) for x in file_types])

print(f"{len(file_types)} filetypes to manage")
print([x[0] for x in file_types])
print(f"{len(dirs_to_create)} directories will be created")
print(f"{files_to_move} files will be moved")

if files_to_move < 1:
    exit()

def create_dir(path_to_dir:str):
    subprocess.run(["mkdir", path_to_dir])

def move_file(file_path:str, dest_path:str):
    subprocess.run(["mv", file_path, dest_path])

for dir, files in file_types:
    target_dir = os.path.join(DOWNLOADS, dir)
    if not os.path.isdir(target_dir):
        create_dir(target_dir)
    for file in files:

        path_to_file = os.path.join(DOWNLOADS, file)
        target_path = os.path.join(target_dir, file)

        if os.path.isfile(path_to_file):
            move_file(path_to_file, target_path)
