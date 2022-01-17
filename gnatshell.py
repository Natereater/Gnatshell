
import datastructures as ds
from colorama import init, Fore, Back, Style
import os


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

# define keyword is used in defining variables, usage: define variable_name value
DEFINE = ["define", "def"]

# variables that can be created
DATAFRAME = "dataframe"
BASIC_PLOT = "basic_plot"
MODEL = "model"
#COLUMN = "column"

VIEW = ["view", "v"]

CLEAR = ["clear", "cls"]

CHANGE_DIRECTORY = "cd"
DIRECTORY = "dir"
LIST_DIRECTORY = "ls"
MAKE_DIRECTORY = "mkdir"
FILE_SYSTEM_COMMANDS = [CHANGE_DIRECTORY, DIRECTORY, LIST_DIRECTORY, MAKE_DIRECTORY]

SET = "set"

NUMERICIZE = "numericize"

CLASSIFY = "classify"

BOOT = "boot"

ADD = "add"
SUB = "sub"
FIT = "fit"







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

def handle_view_command(command: list, memory: ds.MemoryBank):
    """
        Handles define commands
        :param command: the command split on spaces
        :param memory: pointer to the memory bank
        :return: None
    """
    # Set vars
    if len(command) > 2:
        vars = command[2:]
    else:
        vars = None


    # check if command is too short
    if len(command) < 2:
        print_err("ERROR: view needs a variable name")
        return

    # for viewing subsections
    elif "." in command[1]:
        subcommand = command[1].split(".")
        if not memory.var_exists(subcommand[0]):
            print_err("ERROR: " + command[1] + " could not be found in memory")

        # The first part is a valid element in memory
        else:
            view_string = memory.get_var(subcommand[0]).view_subsection(subcommand[1], vars=vars)
            if view_string is not None:
                std_display(view_string)

    # If not in memory at all
    elif not memory.var_exists(command[1]):
        print_err("ERROR: " + command[1] + " could not be found in memory")
        return

    # Handle standard view
    else:
        view_string = memory.get_var(command[1]).view(vars=vars)
        if view_string is not None:
            std_display(view_string)






# Handle defining new variables
def handle_define_command(command: list, memory: ds.MemoryBank):
    """
    Handles define commands
    :param command: the command split on spaces
    :param memory: pointer to the memory bank
    :return: None
    """
    if len(command) < 3:
        print_err("ERROR: define needs a name and a value")
        return

    variable_name = command[1]
    variable = None

    if command[2] == DATAFRAME:
        if len(command) < 4:
            print_err("ERROR: defining a dataframe needs a file path")
            return

        try:
            if len(command) > 4:
                variable = ds.Dataframe(command[3], memory, command[4])
            else:
                variable = ds.Dataframe(command[3], memory)
            memory.add_var(variable_name, variable)
            full_format("<<-- " + variable_name, Fore.MAGENTA)
        except:
            print_err("ERROR: failed to create dataframe")



    elif command[2] == BASIC_PLOT:
        variable = ds.BasicPlot()
        memory.add_var(variable_name, variable)
        full_format("<<-- " + variable_name, Fore.MAGENTA)



    elif command[2] == MODEL:
        if len(command) < 4:
            print_err("ERROR: defining a model needs a dataframe")
            return

        if memory.var_exists(command[3]) and memory.get_var(command[3]).type_string().startswith("dataframe"):
            variable = ds.Model(memory.get_var(command[3]))
            memory.add_var(variable_name, variable)
            full_format("<<-- " + variable_name, Fore.MAGENTA)

        else:
            print_err("ERROR: " + command[3] + " is not a dataframe")


    else:
        print_err("ERROR: " + command[2] + " is not a known data structure")
        return







# Handle all file system commands
def handle_file_commands(command: list, memory: ds.MemoryBank):
    """
    Handles file system commands
    :param command: the command split on spaces
    :param memory: pointer to the memory bank
    :return:
    """
    if command[0] == CHANGE_DIRECTORY:
        if len(command) < 2:
            print_err("ERROR: change directory needs a second argument of a folder, .., or ~")
        else:
            memory.cd(command[1])

    elif command[0] == LIST_DIRECTORY:
        memory.ls()

    elif command[0] == DIRECTORY:
        std_display(memory.dir())

    elif command[0] == MAKE_DIRECTORY:
        if len(command) < 2:
            print_err("ERROR: make directory needs a second argument of a new folder name")
        else:
            memory.mkdir(command[1])





# Handle clearing the terminal
def handle_clear_command(command: list):
    os.system('cls' if os.name == 'nt' else 'clear')
    if len(command) > 1 and command[1] == "+":
        display_header()





def handle_set_command(command: list, memory: ds.MemoryBank):
    """
    Handles altering variables within an item in memory
    :param command:
    :param memory:
    :return:
    """
    if len(command) > 3:
        vars = command[3:]
    else:
        vars = None


    if len(command) < 3:
        print_err("ERROR: set needs a name and a value")
        return


    elif "." not in command[1]:
        print_err("ERROR: object.variable is required when setting variables")
        return


    elif "." in command[1]:
        subcommand = command[1].split(".")
        if not memory.var_exists(subcommand[0]):
            print_err("ERROR: " + command[1] + " could not be found in memory")
            return

        # The first part is a valid element in memory
        else:

            # Check if value in memory
            if memory.var_exists(command[2]):
                # Set with just this variable
                memory.get_var(subcommand[0]).set(subcommand[1], memory.get_var(command[2]), vars)


            # Check if second variable is supposed to be a float
            elif string_is_float(command[2]):
                memory.get_var(subcommand[0]).set(subcommand[1], command[2], vars)


            # Check if value is subsection of memory
            elif "." in command[2]:
                second_subcommand = command[2].split(".")
                if not memory.var_exists(second_subcommand[0]):
                    print_err("ERROR: " + command[2] + " could not be found in memory")
                    return
                else:
                    name = subcommand[1]
                    value = memory.get_var(second_subcommand[0]).get_subsection(second_subcommand[1])
                    if value is not None:
                        memory.get_var(subcommand[0]).set(name, value, vars)


            # Otherwise send as string
            else:
                memory.get_var(subcommand[0]).set(subcommand[1], command[2], vars)








def handle_numericize_command(command: list, memory: ds.MemoryBank):
    """
    Handles numericizing columns
    :param command:
    :param memory:
    :return:
    """
    if len(command) > 2:
        vars = command[2:]
    else:
        vars = None


    if len(command) < 2:
        print_err("ERROR: numericize needs a column to target")
        return

    elif "." not in command[1]:
        print_err("ERROR: dataframe.column_name is required when numericizing a column")
        return

    else:
        subcommand = command[1].split(".")

        if not memory.var_exists(subcommand[0]):
            print_err("ERROR: " + command[1] + " could not be found in memory")
            return

        elif not memory.get_var(subcommand[0]).type_string().startswith("dataframe"):
            print_err("ERROR: " + subcommand[0] + " is not a dataframe")
            return

        else:
            memory.get_var(subcommand[0]).numericize(subcommand[1], vars)







def handle_classify_command(command: list, memory: ds.MemoryBank):
    """
    Handles numericizing columns
    :param command:
    :param memory:
    :return:
    """
    if len(command) > 2:
        vars = command[2:]
    else:
        vars = None


    if len(command) < 2:
        print_err("ERROR: classify needs a column to target")
        return

    elif "." not in command[1]:
        print_err("ERROR: dataframe.column_name is required when classify a column")
        return

    else:
        subcommand = command[1].split(".")

        if not memory.var_exists(subcommand[0]):
            print_err("ERROR: " + command[1] + " could not be found in memory")
            return

        elif not memory.get_var(subcommand[0]).type_string().startswith("dataframe"):
            print_err("ERROR: " + subcommand[0] + " is not a dataframe")
            return

        else:
            memory.get_var(subcommand[0]).classify(subcommand[1], vars)








def handle_add_command(command: list, memory: ds.MemoryBank):
    VALID_TYPES = ["model"]
    valid = False

    if len(command) < 4:
        print_err("ERROR: add needs an input/output tag, a dataframe, and a column name")

    elif command[1] != "input" and command[1] != "output":
        print_err("ERROR: " + command[1] + " must be input or output")


    elif not memory.var_exists(command[2]):

        print_err("ERROR: " + command[2] + " is not a known variable")


    else:
        # Make sure an ML type
        item = memory.get_var(command[2])
        for each in VALID_TYPES:
            if item.type_string().startswith(each):
                valid = True
                break

        if not valid:
            print_err("ERROR: " + command[2] + " is not an ML structure of the set: " + str(VALID_TYPES))
            return

        if command[1] == "input":
            memory.get_var(command[2]).add_input(command[3])
        else:
            memory.get_var(command[2]).add_output(command[3])





def handle_sub_command(command: list, memory: ds.MemoryBank):
    VALID_TYPES = ["model"]
    valid = False

    if len(command) < 4:
        print_err("ERROR: sub needs an input/output tag, a dataframe, and a column name")

    elif command[1] != "input" and command[1] != "output":
        print_err("ERROR: " + command[1] + " must be input or output")

    elif not memory.var_exists(command[2]):
        print_err("ERROR: " + command[2] + " is not a known variable")

    else:
        # Make sure an ML type
        item = memory.get_var(command[2])
        for each in VALID_TYPES:
            if item.type_string().startswith(each):
                valid = True
                break

        if not valid:
            print_err("ERROR: " + command[2] + " is not an ML structure of the set: " + str(VALID_TYPES))
            return


        if command[1] == "input":
            item.remove_input(command[3])
        else:
            item.remove_output(command[3])






def handle_fit_command(command: list, memory: ds.MemoryBank):
    VALID_TYPES = ["model"]
    valid = False

    if len(command) < 2:
        print_err("ERROR: fit needs a target ML structure")
        return

    if not memory.var_exists(command[1]):
        print_err("ERROR: " + command[1] + " is not a known variable in memory")
        return

    item = memory.get_var(command[1])

    for each in VALID_TYPES:
        if item.type_string().startswith(each):
            valid = True
            break

    if not valid:
        print_err("ERROR: " + command[1] + " is not an ML structure of the set: " + str(VALID_TYPES))

    else:
        item.fit()







# Directs the command based on first keyword
def handle_command(command: list, memory: ds.MemoryBank):
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

    elif command[0] in DEFINE:
        handle_define_command(command, memory)

    elif command[0] in VIEW:
        handle_view_command(command, memory)

    elif command[0] in FILE_SYSTEM_COMMANDS:
        handle_file_commands(command, memory)

    elif command[0] in CLEAR:
        handle_clear_command(command)

    elif command[0] == SET:
        handle_set_command(command, memory)

    elif command[0] == NUMERICIZE:
        handle_numericize_command(command, memory)

    elif command[0] == CLASSIFY:
        handle_classify_command(command, memory)

    elif command[0] == ADD:
        handle_add_command(command, memory)

    elif command[0] == SUB:
        handle_sub_command(command, memory)

    elif command[0] == FIT:
        handle_fit_command(command, memory)










# ===========================================
#             MAIN COMMAND LOOP
# ===========================================

def command_loop():
    done = False
    pinned = None
    memory = ds.MemoryBank()

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
