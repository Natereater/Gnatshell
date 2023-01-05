from colorama import init, Fore, Back, Style

colors = {
    "YELLOW": Fore.YELLOW,
    "LIGHTYELLOW": Fore.LIGHTYELLOW_EX,

    "RED": Fore.RED,
    "LIGHTRED": Fore.LIGHTRED_EX,

    "GREEN": Fore.GREEN,
    "LIGHTGREEN": Fore.LIGHTGREEN_EX,

    "BLUE": Fore.BLUE,
    "LIGHTBLUE": Fore.LIGHTBLUE_EX,

    "BLACK": Fore.BLACK,
    "LIGHTBLACK": Fore.LIGHTBLACK_EX,

    "WHITE": Fore.WHITE,
    "LIGHTWHITE": Fore.LIGHTWHITE_EX,

    "CYAN": Fore.CYAN,
    "LIGHTCYAN": Fore.LIGHTCYAN_EX,

    "MAGENTA": Fore.MAGENTA,
    "LIGHTMAGENTA": Fore.LIGHTMAGENTA_EX,
}



names = {
    "YAKS ETERNAL": Fore.YELLOW,
    "CROWNE EMPIRIUM": Fore.LIGHTYELLOW_EX,

    "WESTINTON WERERABBITS": Fore.RED,
    "VYLERIN VAMPARROTS": Fore.LIGHTRED_EX,

    "NOT BROCCOLI": Fore.GREEN,
    "QUASIBROCCOLI UNITED": Fore.LIGHTGREEN_EX,

    "DEEPWATER SEACLAN": Fore.BLUE,
    "MASTONIA MAGES": Fore.LIGHTBLUE_EX,

    "DARKNESS INCARNATE": Fore.BLACK,
    "HADES SNOWBALLS": Fore.LIGHTBLACK_EX,

    "POLAR MOOSEGANG": Fore.WHITE,
    "TITANVILLE TOASTERS": Fore.LIGHTWHITE_EX,

    "EASTINTON TIMEWARDENS": Fore.CYAN,
    "ASTRALION UNITED": Fore.LIGHTCYAN_EX,

    "THE PENGUIN ITSELF": Fore.MAGENTA,
    "WOOLVIEW WIZARDS": Fore.LIGHTMAGENTA_EX,
}


for color in colors.keys():
    print(colors[color] + color)

print(Fore.RESET + "\n\n")

for name in names.keys():
    print(names[name] + name)

print(Fore.RESET + "\n\n")