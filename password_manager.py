from data_files_util import Datafile
from colorama import Fore

FILENAME = "passwd.txt"
KEY_FILE = "key.key"

VIEW = "v"
ADD = "add"
DELETE = "del"
SAVE = "save"
HELP = "help"

def print_err(text):
    print(Fore.RED + text)



class PasswordManager:
    def __init__(self, password_file: str, key_file: str):
        self.pwd = Datafile(password_file, key=key_file)

    def view(self, vars=None) -> str:
        if vars is not None and len(vars) > 0:
            return self.pwd.view_specific(vars[0])
        else:
            return self.pwd.view()

    def add(self, command: list):
        if len(command) < 4:
            print_err("ERROR: invalid add, must have name and value")
        else:
            self.pwd.add(name=command[2], value=command[3], is_encrypted=True, tag="encrypted")

    def delete(self, command: list):
        if len(command) < 3:
            print_err("ERROR: invalid delete, must have name")
        else:
            self.pwd.delete(command[2])

    def save(self):
        self.pwd.save()

    def type_string(self) -> str:
        return "password_manager"


    def help(self) -> str:
        build_str = ""
        build_str += Fore.LIGHTBLUE_EX
        build_str += "PASSWORD MANAGER:\n"
        build_str += "This tool allows you to store, view, and edit encrypted passwords.\n\n"
        build_str += "VIEW ALL PASSWORDS:\n" + Fore.LIGHTGREEN_EX + "passwd v" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW A SPECIFIC PASSWORD:\n" + Fore.LIGHTGREEN_EX + "passwd v [name]" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "ADD A PASSWORD:\n" + Fore.LIGHTGREEN_EX + "passwd add [name] [value]" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "DELETE A PASSWORD:\n" + Fore.LIGHTGREEN_EX + "passwd del [name]" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "SAVE ALL CHANGES:\n" + Fore.LIGHTGREEN_EX + "passwd save" + Fore.LIGHTBLUE_EX + "\n\n"
        return build_str

    def handle(self, command:list):
        if len(command) < 2:
            return

        if command[1] == VIEW and len(command) > 2:
            print(self.view(vars=command[2:]))
        elif command[1] == VIEW:
            print(self.view())
        elif command[1] == ADD:
            self.add(command)
        elif command[1] == DELETE:
            self.delete(command)
        elif command[1] == SAVE:
            self.save()
        elif command[1] == HELP:
            print(self.help())
        else:
            print_err("ERROR: unknown password manager command: " + command[1])


