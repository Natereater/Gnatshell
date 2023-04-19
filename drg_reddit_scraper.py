import praw
from colorama import Fore
import pandas as pd
from tabulate import tabulate



CLIENT_ID = "ITmq-ySQlTM1bvjzMhAW-w"
CLIENT_SECRET = "2NU4tgI1bpGAhOPKuNvVAG0iI6Bakw"
USERNAME = "Eiseneater"
USER_AGENT = "gnatshell/1.0"

VIEW = "v"
HELP = "help"


BIOMES = {
    'Fungus Bogs' : Fore.LIGHTGREEN_EX,
    'Hollow Bough': Fore.RED,
    'Crystalline Caverns': Fore.LIGHTBLUE_EX,
    'Glacial Strata': Fore.LIGHTWHITE_EX,
    'Salt Pits': Fore.LIGHTRED_EX,
    'Dense Biozone': Fore.CYAN,
    'Radioactive Exclusion Zone': Fore.GREEN,
    'Magma Core': Fore.YELLOW,
    'Sandblasted Corridors': Fore.LIGHTYELLOW_EX,
    'Azure Weald': Fore.MAGENTA
}



def print_err(text):
    print(Fore.RED + text + Fore.RESET)


class DRGRedditScraper:

    def __init__(self):
        self.password = None


    def get_deep_dives(self) -> str:
        try:
            if self.password is None:
                self.password = input("Please enter password: ")

            # Authenticate with Reddit's API
            reddit = praw.Reddit(client_id=CLIENT_ID,
                                 client_secret=CLIENT_SECRET,
                                 username=USERNAME,
                                 password=self.password,
                                 user_agent=USER_AGENT)

            # Get the subreddit object
            subreddit = reddit.subreddit('deeprockgalactic')

            # Get the pinned post object
            pinned_post = subreddit.sticky()

            # Get the text of the pinned post
            pinned_post_text = pinned_post.selftext

            # Print the text of the pinned post
            return pinned_post_text
        except:
            print_err("ERROR: could not retrieve deep dives")



    def get_formatted_deep_dives(self) -> str:
        base = self.get_deep_dives()

        dd_title = ""
        edd_title = ""

        dd_stage = []
        dd_primary = []
        dd_secondary = []
        dd_anomaly = []
        dd_warning = []

        edd_stage = []
        edd_primary = []
        edd_secondary = []
        edd_anomaly = []
        edd_warning = []



        try:
            parts = base.split("\n")
            i = 0
            while i < len(parts):
                if parts[i].startswith("**"):
                    dd_title = parts[i][2:len(parts[i]) - 2]
                    i += 1
                    break
                i += 1

            while i < len(parts):
                if parts[i].startswith("**"):
                    break
                elif parts[i].startswith("|1") or parts[i].startswith("|2") or parts[i].startswith("|3"):
                    table_line = parts[i].split("|")
                    dd_stage.append(table_line[1])
                    dd_primary.append(table_line[2])
                    dd_secondary.append(table_line[3])
                    dd_anomaly.append(table_line[4])
                    dd_warning.append(table_line[5])
                i += 1

            while i < len(parts):
                if parts[i].startswith("**"):
                    edd_title = parts[i][2:len(parts[i]) - 2]
                    i += 1
                    break
                i += 1

            while i < len(parts):
                if parts[i].startswith("|1") or parts[i].startswith("|2") or parts[i].startswith("|3"):
                    table_line = parts[i].split("|")

                    edd_stage.append(table_line[1])
                    edd_primary.append(table_line[2])
                    edd_secondary.append(table_line[3])
                    edd_anomaly.append(table_line[4])
                    edd_warning.append(table_line[5])
                if parts[i].startswith("|3"):
                    break
                i += 1

            # Build output
            buildstring = "\n"

            for biome in BIOMES:
                if biome in dd_title:
                    buildstring += BIOMES[biome]

            buildstring += dd_title + "\n\n"
            df = pd.DataFrame({'STAGE': dd_stage,
                               'PRIMARY': dd_primary,
                               'SECONDARY': dd_secondary,
                               'ANOMALY': dd_anomaly,
                               'WARNING': dd_warning})
            buildstring += tabulate(df, headers='keys', tablefmt='fancy_grid')
            buildstring += "\n\n\n" + Fore.RESET

            for biome in BIOMES:
                if biome in edd_title:
                    buildstring += BIOMES[biome]

            buildstring += edd_title + "\n\n"
            df = pd.DataFrame({'STAGE': edd_stage,
                               'PRIMARY': edd_primary,
                               'SECONDARY': edd_secondary,
                               'ANOMALY': edd_anomaly,
                               'WARNING': edd_warning})
            buildstring += tabulate(df, headers='keys', tablefmt='fancy_grid')
            buildstring += "\n\n"  + Fore.RESET

            return buildstring

        except:
            print_err("ERROR: Failure to format deep dives")


    def type_string(self) -> str:
        return "drg_tool"

    def view(self, vars=None) -> str:
        if vars is not None and len(vars) > 0 and vars[0] == 'raw':
            return self.get_deep_dives()
        else:
            return self.get_formatted_deep_dives()


    def help(self) -> str:
        build_str = ""
        build_str += Fore.LIGHTBLUE_EX
        build_str += "DEEP ROCK GALACTIC TOOL:\n"
        build_str += "Can be used to view this weeks deep dives for Deep Rock Galactic.\n\n"
        build_str += "VIEW THIS WEEKS DEEP DIVES:\n" + Fore.LIGHTGREEN_EX + "drg v" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW THIS WEEKS DEEP DIVES RAW FROM REDDIT:\n" + Fore.LIGHTGREEN_EX + "drg v raw" \
                     + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += Fore.RESET
        return build_str

    def handle(self, command:list):
        if len(command) < 2:
            return

        if command[1] == VIEW and len(command) > 2:
            print(self.view(vars=command[2:]))

        elif command[1] == VIEW:
            print(self.view())

        elif command[1] == HELP:
            print(self.help())

        else:
            print_err("ERROR: unknown drg command: " + command[1])



