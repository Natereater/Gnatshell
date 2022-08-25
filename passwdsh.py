from data_files_util import Datafile

FILENAME = "passwd.txt"
KEY_FILE = "key.key"

VIEW = "view"
ADD = "add"
DELETE = "del"
SAVE = "save"
EXIT = "exit"


def handle_view(command:str, pwd:Datafile):
    split = command.split(" ")
    if len(split) > 1:
        pwd.view_specific(split[1])
    else:
        pwd.view()


def handle_add(command:str, pwd:Datafile):
    split = command.split(" ")
    if len(split) < 3:
        print("ERROR: invalid add, must have name and value")
    else:
        pwd.add(name=split[1], value=split[2], is_encrypted=True, tag="encrypted")


def handle_delete(command:str, pwd:Datafile):
    split = command.split(" ")
    if len(split) < 2:
        print("ERROR: invalid delete, must have name")
    else:
        pwd.delete(split[1])


def handle_save(pwd:Datafile):
    pwd.save()



def command_loop():
    pwd = Datafile(FILENAME, key=KEY_FILE)
    keep_running = True

    while(keep_running):

        command = input("[PASSWDSH]> ").strip()

        if command.startswith(VIEW):
            handle_view(command, pwd)
        elif command.startswith(ADD):
            handle_add(command, pwd)
        elif command.startswith(DELETE):
            handle_delete(command, pwd)
        elif command.startswith(SAVE):
            handle_save(pwd)
        elif command.startswith(EXIT):
            keep_running = False

if __name__ == "__main__":
    command_loop()