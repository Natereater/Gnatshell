import requests
from colorama import Fore
import json
from bs4 import BeautifulSoup

WIKI_URL = "https://en.wikipedia.org/api/rest_v1/page/mobile-sections/"


def print_err(text):
    print(Fore.RED + text + Fore.RESET)



class Wikipedia:

    def __init__(self):
        pass

    def get_summary(self, title: str) -> str:
        try:
            response = requests.get(WIKI_URL + title)

            # extract the sections from the response JSON
            summary = response.json()["lead"]["sections"][0]["text"]
            sections = response.json()["remaining"]["sections"]

            buildstring = Fore.LIGHTYELLOW_EX + title.upper() + "\n\n"
            buildstring += Fore.LIGHTMAGENTA_EX + BeautifulSoup(summary, "html.parser").get_text()

            # loop through the sections and extract the plain text
            for section in sections:
                # use BeautifulSoup to parse the HTML and extract the text
                if "anchor" in section and section["anchor"] != "References":
                    buildstring += "\n\n" + Fore.LIGHTBLUE_EX + section["anchor"] + Fore.LIGHTMAGENTA_EX
                    soup = BeautifulSoup(section["text"], "html.parser")
                    text = soup.get_text()
                    buildstring += "\n" + text


            # extract the summary from the response JSON=
            return buildstring + Fore.RESET
        except:
            print_err("ERROR: " + title + " not found.")



wiki = Wikipedia()

print(wiki.get_summary("Dunrobin Castle"))
print("--------------------")
print(wiki.get_summary("Hyper Light Drifter"))

