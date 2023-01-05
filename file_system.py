
from colorama import init, Fore, Back, Style
import os
import re


def print_err(text):
    print(Fore.RED + text)


class FolderStructure:

    def __init__(self, base: str):
        self.base = base
        self.cwd = "~"


    def cd(self, path:str):
        if path == "..":
            if self.cwd != "~":
                split_up = self.cwd.split("/")
                self.cwd = ""
                for i in range(len(split_up) - 1):
                    self.cwd += split_up[i]
                    if i < len(split_up) - 2:
                        self.cwd += "/"

        elif path == "~":
            self.cwd = "~"

        else:
            full_path = self.cwd.replace("~", self.base)
            full_path = full_path + "/" + path
            if os.path.isdir(full_path):
                self.cwd = self.cwd + "/" + path
            else:
                print_err("ERROR: " + self.cwd + "/" + path + " is not an existing directory")



    def pwd(self) -> str:
        return self.cwd


    def ls(self):
        full_path = self.cwd.replace("~", self.base)
        full_list = os.listdir(full_path)

        for element in full_list:
            if os.path.isdir(os.path.join(full_path, element)):
                print(Fore.LIGHTMAGENTA_EX + element)
            else:
                print(Fore.LIGHTBLUE_EX + element)


    # TODO: implement make directory
    def mkdir(self, dir_name:str):
        pass


    def type_string(self) -> str:
        return "folder_structure"


    def __recursive_view_files(self, build_string: str, full_path: str, num_indents: int) -> str:
        full_list = os.listdir(full_path)

        for element in full_list:
            if os.path.isdir(os.path.join(full_path, element)):
                build_string += Fore.RESET + ("| " * (num_indents - 1)) + ("┕ " if num_indents > 0 else "") + Fore.LIGHTMAGENTA_EX + element + "\n"
                build_string += self.__recursive_view_files("", full_path + "/" + element, num_indents + 1)
            else:
                build_string += Fore.RESET + ("| " * (num_indents - 1)) + ("┕ " if num_indents > 0 else "") + Fore.LIGHTBLUE_EX + element + "\n"
        return build_string


    def view(self, vars=None) -> str:
        full_path = self.cwd.replace("~", self.base)
        build_string = self.__recursive_view_files("", full_path, 0)
        return build_string

    def handle(self, command:list):
        pass


