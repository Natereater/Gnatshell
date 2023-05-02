import requests
from typing import List, Optional
import random
import html
from colorama import Fore

DIFFICULTIES = [
    "easy",
    "medium",
    "hard"
]

OPTIONS = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
}

CATEGORIES = {
    "9": "General Knowledge",
    "10": "Books",
    "11": "Film",
    "12": "Music",
    "13": "Theatre",
    "14": "Television",
    "15": "Video Games",
    "16": "Board Games",
    "17": "Science and Nature",
    "18": "Computer Science",
    "19": "Mathematics",
    "20": "Mythology",
    "21": "Sports",
    "22": "Geography",
    "23": "History",
    "24": "Politics",
    "25": "Art",
    "26": "Celebrities",
    "27": "Animals"
}

VIEW = "view"
GET = "get"
HELP = "help"


def print_err(text):
    print(Fore.RED + text)


def get_trivia(amount, difficulty, category=None):
    url = "https://opentdb.com/api.php?"
    url += "amount=" + amount
    if category is not None:
        url += "&category=" + category
    url += "&difficulty=" + difficulty + "&type=multiple"
    response = requests.get(url)
    return response.json()["results"]




class Question:
    def __init__(self, json_in):
        self.question = html.unescape(json_in["question"])
        self.answer = json_in["correct_answer"]
        self.options: List = json_in["incorrect_answers"]
        self.options.append(self.answer)
        random.shuffle(self.options)

    def pose(self):
        print("\n" + self.question)
        for option in OPTIONS.keys():
            print("[" + option + "] " + html.unescape(self.options[OPTIONS[option]]))
        print()
        answer = input("Enter your answer: ").upper()

        if answer in OPTIONS and self.options[OPTIONS[answer]] == self.answer:
            print(Fore.LIGHTGREEN_EX + "CORRECT" + Fore.RESET)
        else:
            print(Fore.RED + "INCORRECT" + Fore.RESET)
            print("Correct Answer: " + html.unescape(self.answer))
        print("\n\n")



class Trivia:

    def __init__(self):
        self.questions = []

    def run_trivia(self, amount, difficulty, category=None):
        if difficulty not in DIFFICULTIES:
            print_err("ERROR: " + difficulty + " is not a valid difficulty: (easy, medium, hard)")

        try:
            self.questions = []
            response = get_trivia(amount=amount, difficulty=difficulty, category=category)
            for item in response:
                self.questions.append(Question(item))
        except:
            print_err("ERROR: Failed to get questions")

        for question in self.questions:
            question.pose()


    def type_string(self) -> str:
        return "trivia_game"


    def help(self) -> str:
        build_str = ""
        build_str += Fore.LIGHTBLUE_EX
        build_str += "TRIVIA GAME:\n"
        build_str += "This tool can provide trivia questions on a variety of subjects.\n\n"
        build_str += "GET 1 RANDOM TRIVIA QUESTION:\n" + Fore.LIGHTGREEN_EX + "trivia v" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "GET TRIVIA QUESTIONS:\n" + Fore.LIGHTGREEN_EX + \
                     "trivia get [category] [number_of_questions] [difficulty]" + Fore.LIGHTBLACK_EX + "\n\n"
        build_str += "CATEGORIES:\n"
        for item in CATEGORIES:
            build_str += "\t[" + item + "] " + CATEGORIES[item] + "\n"
        build_str += "\n"

        build_str += "DIFFICULTIES:\n\teasy\n\tmedium\n\thard\n\n"
        build_str += Fore.RESET
        return build_str


    def view(self, vars=None) -> str:
        buildstring = ""
        diff = random.choice(DIFFICULTIES)
        self.run_trivia(amount="1", difficulty=diff)
        return buildstring


    def handle(self, command:list):
        if len(command) < 2:
            return

        if command[1] == VIEW and len(command) > 2:
            print(self.view(vars=command[2:]))

        elif command[1] == VIEW:
            print(self.view())

        elif command[1] == HELP:
            print(self.help())

        elif command[1] == GET:
            if len(command) < 5:
                print_err("ERROR: get command requires a category, # of questions, and difficulty")
                return
            if command[2] not in CATEGORIES.keys():
                print_err("ERROR: " + command[2] + " is not a valid category")
                return
            if command[4] not in DIFFICULTIES:
                print_err("ERROR: " + command[4] + " is not a valid difficulty (easy, medium, hard)")
                return
            try:
                num = int(command[3])
                if num <= 0 or num >= 51:
                    print_err("ERROR: amount must be an integer from 1 to 50.")
                    return
            except:
                print_err("ERROR: amount must be an integer from 1 to 50.")
                return

            self.run_trivia(amount=command[3], difficulty=command[4], category=command[2])

        else:
            print_err("ERROR: unknown trivia command: " + command[1])



