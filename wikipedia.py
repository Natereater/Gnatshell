import requests
from colorama import Fore
import json
from bs4 import BeautifulSoup

WIKI_URL = "https://en.wikipedia.org/api/rest_v1/page/mobile-sections/"
RAND_URL = "https://en.wikipedia.org/w/api.php?action=query&list=random&format=json&rnnamespace=0&rnlimit=1"

VIEW = "v"
SUMMARY = "summ"
FULL = "full"
HELP = "help"



def print_err(text):
    print(Fore.RED + text + Fore.RESET)



class Wikipedia:

    def __init__(self):
        pass

    def get_full_article(self, title: str) -> str:
        try:
            response = requests.get(WIKI_URL + title)

            # extract the sections from the response JSON
            summary = response.json()["lead"]["sections"][0]["text"]
            sections = response.json()["remaining"]["sections"]

            buildstring = Fore.LIGHTYELLOW_EX + title.upper() + "\n\n"
            buildstring += Fore.LIGHTCYAN_EX + BeautifulSoup(summary, "html.parser").get_text()

            # loop through the sections and extract the plain text
            for section in sections:
                # use BeautifulSoup to parse the HTML and extract the text
                if "anchor" in section and section["anchor"] != "References":
                    buildstring += "\n\n" + Fore.LIGHTBLUE_EX + section["anchor"] + Fore.LIGHTCYAN_EX
                    soup = BeautifulSoup(section["text"], "html.parser")
                    text = soup.get_text()
                    buildstring += "\n" + text


            # extract the summary from the response JSON=
            return buildstring + Fore.RESET
        except:
            print_err("ERROR: " + title + " not found.")


    def get_summary(self, title: str) -> str:
        try:
            response = requests.get(WIKI_URL + title)

            # extract the sections from the response JSON
            summary = response.json()["lead"]["sections"][0]["text"]

            buildstring = Fore.LIGHTYELLOW_EX + title.upper() + "\n\n"
            buildstring += Fore.LIGHTCYAN_EX + BeautifulSoup(summary, "html.parser").get_text()

            # extract the summary from the response JSON=
            return buildstring + Fore.RESET
        except:
            print_err("ERROR: " + title + " not found.")


    def get_random(self) -> str:
        response = requests.get(RAND_URL)
        title = response.json()["query"]["random"][0]["title"]
        return self.get_summary(title)

    def get_random_full(self) -> str:
        response = requests.get(RAND_URL)
        title = response.json()["query"]["random"][0]["title"]
        return self.get_full_article(title)



    def type_string(self) -> str:
        return "wikipedia_tool"


    def view(self, vars=None) -> str:
        if vars is not None and len(vars) > 0:
            return self.get_random_full()
        else:
            return self.get_random()


    def help(self) -> str:
        build_str = ""
        build_str += Fore.LIGHTBLUE_EX
        build_str += "WIKIPEDIA TOOL:\n"
        build_str += "This tool allows the user to read wikipedia articles and summaries\n\n"
        build_str += "VIEW RANDOM SUMMARY:\n" + Fore.LIGHTGREEN_EX + "wiki v" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW RANDOM FULL ARTICLE:\n" + Fore.LIGHTGREEN_EX + "wiki v full" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW SUMMARY:\n" + Fore.LIGHTGREEN_EX + "wiki summ [title]" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW FULL ARTICLE:\n" + Fore.LIGHTGREEN_EX + "wiki full [title]" + Fore.LIGHTBLUE_EX + "\n\n"
        return build_str



    def handle(self, command:list):
        if len(command) < 2:
            return

        if command[1] == VIEW and len(command) > 2:
            print(self.view(vars=command[2:]))

        elif command[1] == VIEW:
            print(self.view())

        elif command[1] == SUMMARY:
            if len(command) < 3:
                print_err("ERROR: summary command requires a title to search by")
            else:
                print(self.get_summary(command[2]))

        elif command[1] == FULL:
            if len(command) < 3:
                print_err("ERROR: full command requires a title to search by")
            else:
                print(self.get_full_article(command[2]))

        elif command[1] == HELP:
            print(self.help())





