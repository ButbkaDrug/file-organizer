#! /bin/python3
import os
import subprocess
from sys import stderr
import argparse

class FileManager:
    def __init__(
        self,
        sourse,
        threshold = 2
    ):
        if not os.path.isdir(sourse):
            print(f"ERROR: {sourse} is not a directory. Exiting")
            exit(1)
        self.source = sourse
        self.threshold = threshold
        self.list_of_files = os.listdir(self.source)
        self.extensions = {}

    def create_dir(self, path_to_dir:str):
        subprocess.run(["mkdir", path_to_dir])

    def move_file(self, file_path:str, dest_path:str):
        subprocess.run(["mv", file_path, dest_path])

    def get_extensions(self):

        numbers = range(ord("1"), ord("9"))
        letters = range(ord("A"), ord("z"))


        for file in self.list_of_files:
            if os.path.isdir(os.path.join(self.source, file)):
                continue

            index = file.rfind(".")
            ext = file[index+1:]

            if len(ext) < 2 and ext not in numbers and ext not in letters:
                continue

            if ext not in self.extensions:
                self.extensions.update({ext:[file]})
            else:
                self.extensions[ext].append(file)

    def get_stats(self):
        self.file_types = [x for x in self.extensions.items() if len(x[1]) > self.threshold]
        self.dirs_to_create = [x[0] for x in self.file_types if not os.path.isdir(x[0])]
        self.files_to_move = sum([len(x[1]) for x in self.file_types])

    def print_stats(self):

        print(f"Directory {self.source}")
        print(f"Total items: {len(self.list_of_files)}")
        print(f"Total types: {len(self.extensions)}")


        print(f"{len(self.file_types)} filetypes to manage")
        print(f"{len(self.dirs_to_create)} directories will be created")
        print(f"{self.files_to_move} files will be moved")

    def run(self):

        self.get_extensions()

        self.get_stats()

        self.print_stats()

        if self.files_to_move < 1:
            print("There is nothig I can do for you... Exiting")
            exit()


        for dir, files in self.file_types:
            target_dir = os.path.join(self.source, dir)
            if not os.path.isdir(target_dir):
                self.create_dir(target_dir)
            for file in files:

                path_to_file = os.path.join(self.source, file)
                target_path = os.path.join(target_dir, file)

                if os.path.isfile(path_to_file):
                    self.move_file(path_to_file, target_path)

    def run_test(self):
        self.get_extensions()
        self.get_stats()
        self.print_stats()

        if self.files_to_move < 1:
            print("This directory seems fine. Nothing is there to move")

        print("Changes preview:")

        for dir, files in self.file_types:
            target_dir = os.path.join(self.source, dir)
            print(f"{len(files)} will be moved into {target_dir}")
            for file in files:
                print(f"\t{file}")






def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "path",
        type=str,
        help="Path to a directory you want to organize"
    )

    parser.add_argument(
        "-t",
        "--test",
        help="Run a test. Without moving any files",
        action="store_true",
    )

    args = parser.parse_args()

    fm = FileManager(args.path)

    if args.test:
        fm.run_test()
    else:
        fm.run()






if __name__ == "__main__":
    main()
