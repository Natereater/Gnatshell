
from colorama import init, Fore, Back, Style
import file_system
import data_files_util as dfu
import os
import password_manager
from dataframe_tool import Dataframe
from iaaf_converter import IaafConverter



# initialize colorama
init(convert=True, autoreset=True)



# used to print error messages
def print_err(text):
    print(Fore.RED + text)


RESERVED = ["cd", "ls", "pwd", "mkdir", "v", "view", "cls", "pin"]






# ===========================================
#                MEMORY BANK
# ===========================================
class MemoryBank:
    """
    Class that defines all storage of variables
    """

    def __init__(self, settings: dfu.Datafile):
        self.variables = dict()
        self.variables["mem"] = self
        self.variables["settings"] = settings
        self.variables["base"] = file_system.FolderStructure(settings.get("base"))
        self.variables["passwd"] = password_manager.PasswordManager(settings.get("passwd_file"),
                                                                    settings.get("passwd_key"))
        self.variables["wa"] = IaafConverter()


    def var_exists(self, key: str) -> bool:
        return key in self.variables.keys()


    def get_var(self, key: str):
        return self.variables[key]


    def type_string(self) -> str:
        return "memory_bank"


    def add_var(self, key: str, value):
        if self.var_exists(key) or key in RESERVED:
            print_err("ERROR: " + key + " is a taken or reserved variable name in memory")
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
            build_string += Fore.LIGHTRED_EX + var + Fore.RESET + " : " + Fore.LIGHTYELLOW_EX + \
                            self.variables[var].type_string() + "\n"
        return build_string


    def view_subsection(self, subsection, vars=None) -> str:
        if subsection in self.variables.keys():
            return self.variables[subsection].view(vars=vars)
        else:
            print_err("ERROR: " + subsection + " does not exist in memory")


    def cd(self, path:str):
        self.variables["base"].cd(path)


    def pwd(self) -> str:
        return self.variables["base"].pwd()


    def ls(self):
        self.variables["base"].ls()


    def mkdir(self, dir_name:str):
        self.variables["base"].mkdir(dir_name)


    def handle(self, command:list):
        if command[0] in RESERVED:

            if command[0] == "pwd":
                print(self.pwd())

            elif command[0] == "v" or command[0] == "view":
                if len(command) < 2:
                    print(self.view())
                else:
                    vars = None
                    if len(command) > 2:
                        vars = command[2:]
                    print(self.view_subsection(command[1], vars=vars))

            elif command[0] == "ls":
                self.ls()

            elif command[0] == "cd":
                if len(command) < 2:
                    print_err("ERROR: changing directory requires a path")
                else:
                    self.cd(command[1])

            elif command[0] == "mkdir":
                if len(command) < 2:
                    print_err("ERROR: making a directory requires a directory name")
                else:
                    self.mkdir(command[1])

            elif command[0] == "cls":
                os.system('cls' if os.name == 'nt' else 'clear')

            elif command[0] == "pin":
                if len(command) < 3:
                    print_err("ERROR: pinning requires a name and a value")
                else:
                    var_name = command[1]
                    var_value: str = command[2]

                    if var_value.endswith(".csv") or var_value.endswith(".tsv"):
                        try:
                            new_var = None
                            if len(command) > 3:
                                new_var = Dataframe(csv_name=var_value, memory_bank=self, delimeter=command[3])
                            else:
                                new_var = Dataframe(csv_name=var_value, memory_bank=self)
                            self.add_var(var_name, new_var)
                            print(Fore.LIGHTGREEN_EX + "+ " + var_name + Fore.RESET)
                        except:
                            print_err("ERROR: could not read file: " + command[2])

        else:
            if command[0] in self.variables.keys() and command[0] != "mem":
                self.variables[command[0]].handle(command)








