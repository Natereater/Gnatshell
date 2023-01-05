
import memory_bank as mb
from colorama import init, Fore, Back, Style
import os
import data_files_util as dfu


# initialize colorama
init(convert=True, autoreset=True)

PROMPT_START_PAR = "["
LOCAL_PROGRAM = "GNAT"
PROMPT_END_PAR = "]"
PROMPT_SYMBOL = " >> "



# ===========================================
#                  KEYWORDS
# ===========================================
EXIT = "exit"










# ===========================================
#              GLOBAL FUNCTIONS
# ===========================================

def print_err(text):
    print(Fore.RED + text)


def std_display(text):
    print(Fore.YELLOW + text)


def full_format(text, fore_color, back_color=Back.BLACK, end="\n"):
    print(fore_color + back_color + text, end=end)


def display_header():
    header_file = open("shell_header.txt", "r")
    full_format(header_file.read(), Fore.GREEN)



def string_is_float(string: str) -> bool:
    try:
        x = float(string)
        return True
    except:
        return False








# ===========================================
#              COMMAND HANDLERS
# ===========================================
def handle_boot_command(command: list, memory: mb.MemoryBank):
    pass






# Directs the command based on first keyword
def handle_command(command: list, memory: mb.MemoryBank):
    """
    Handles command sent from command loop
    :param command: the command split on spaces
    :param memory: pointer to the memory bank
    :return: None
    """
    if len(command) < 1:
        print_err("ERROR: No command")
        return

    if command[0] == EXIT:
        exit(0)

    else:
        memory.handle(command)










# ===========================================
#             MAIN COMMAND LOOP
# ===========================================

def command_loop():
    done = False
    pinned = None
    settings = dfu.Datafile("settings.txt")
    memory = mb.MemoryBank(settings)

    while not done:
        full_format(PROMPT_START_PAR, Fore.GREEN, end="")
        full_format(LOCAL_PROGRAM, Fore.WHITE, end="")
        full_format(PROMPT_END_PAR, Fore.GREEN, end="")
        if pinned is not None:
            full_format(PROMPT_START_PAR, Fore.GREEN, end="")
            full_format(pinned, Fore.WHITE, end="")
            full_format(PROMPT_END_PAR, Fore.GREEN, end="")
        full_format(PROMPT_SYMBOL, Fore.GREEN, end="")
        command = input("")

        handle_command(command.split(" "), memory)





def main():
    display_header()
    command_loop()





if __name__ == "__main__":
    main()
