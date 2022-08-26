
from colorama import init, Fore, Back, Style
import pandas as pd
import file_system
import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like
import numpy as np



# initialize colorama
init(convert=True, autoreset=True)



# used to print error messages
def print_err(text):
    print(Fore.RED + text)



# ===========================================
#                 SETTINGS
# ===========================================
class Settings:
    """
    Settings:

    base: the base file folder for files to be stored
    """
    def __init__(self):
        self.settings = dict()
        settings_file = open("settings.txt", "r")
        for line in settings_file:
            subline = line.split(">")
            if len(subline) == 2:
                value = subline[1]
                if value.endswith("\n"):
                    value = value[:-1]
                self.settings[subline[0]] = value

    def get_setting(self, key: str) -> str:
        if key in self.settings.keys():
            return self.settings[key]
        else:
            print_err("ERROR: " + key + " is not a valid setting")




# Instantiate a global settings instance
GLOBAL_SETTINGS = Settings()










# ===========================================
#                MEMORY BANK
# ===========================================
class MemoryBank:
    """
    Class that defines all storage of variables
    """

    def __init__(self):
        self.variables = dict()
        self.variables["mem"] = self
        self.variables["base"] = file_system.FolderStructure(GLOBAL_SETTINGS.get_setting("base"))


    def var_exists(self, key: str) -> bool:
        return key in self.variables.keys()


    def get_var(self, key: str):
        return self.variables[key]


    def type_string(self) -> str:
        return "memory_bank"


    def add_var(self, key: str, value):
        if self.var_exists(key):
            print_err("ERROR: " + key + " is a taken variable name in memory")
        else:
            self.variables[key] = value


    def get_subsection(self, subsection: str):
        if self.var_exists(subsection):
            return self.get_var(subsection)
        else:
            print_err("ERROR: " + subsection + " does not exist")
            return None


    def view(self, vars=None) -> str:
        build_string = ""
        for var in self.variables.keys():
            build_string += var + " : " + self.variables[var].type_string() + "\n"
        return build_string


    def view_subsection(self, subsection, vars=None) -> str:
        if subsection in self.variables.keys():
            return self.variables[subsection].view(vars=vars)
        else:
            print_err("ERROR: " + subsection + " does not exist in memory")


    def cd(self, path:str):
        self.variables["base"].cd(path)


    def dir(self) -> str:
        return self.variables["base"].dir()


    def ls(self):
        self.variables["base"].ls()


    def mkdir(self, dir_name:str):
        self.variables["base"].mkdir(dir_name)

    def set(self, name: str, value, vars=None):
        print_err("ERROR: memory_bank does not implement setting variables")







