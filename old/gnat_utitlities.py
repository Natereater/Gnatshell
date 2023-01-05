from colorama import init, Fore, Back, Style
import cmd


def print_in_box(header: str, body: str, box_color=Fore.YELLOW):
    pass



import curses

screen = curses.initscr()
screen.addstr("Hello World!!!\nfoovvar\n\n\nwow")
screen.refresh()
screen.getch()
curses.endwin()
