import csv
from typing import Dict, Union
import math
from colorama import Fore



VIEW = "v"

CONVERT = "convert"
MARK = "mark"
POINTS = "points"
SPREAD = "spread"
HELP = "help"


def print_err(text):
    print(Fore.RED + text)



class IaafTableValue:
    def __init__(self, a:float, b:float, c:float, time:bool, integer:bool):
        self.a = a
        self.b = b
        self.c = c
        self.time = time
        self.integer = integer


    def get_points(self, mark:float) -> int:
        points = self.a * ((mark + self.b) ** 2) + self.c
        return int(points)


    def get_mark(self, points:int) -> Union[int, float]:
        if self.time:
            if self.integer:
                return math.floor((-self.a * self.b - math.sqrt(-self.a * (self.c - points))) / self.a)
            else:
                mark = math.floor((-self.a * self.b - math.sqrt(-self.a * (self.c - points))) / self.a * 100)
                return mark / 100
        else:
            if self.integer:
                return math.floor(math.sqrt((points - self.c) / self.a) - self.b)
            else:
                mark = math.floor((math.sqrt((points - self.c) / self.a) - self.b) * 100)
                return mark / 100


    def get_formatted_mark(self, points:int) -> str:
        mark = self.get_mark(points)
        if self.time and mark > 60:
            minutes = mark // 60
            seconds = mark % 60
            if minutes > 60:
                hours = minutes // 60
                minutes = minutes % 60
                return str(int(hours)) + ":" + f"{int(minutes):02}" + ":" + str(round(seconds, 2))
            else:
                return str(int(minutes)) + ":" + ("" if seconds >= 10 else "0") + str(round(seconds, 2))
        else:
            return str(round(mark, 2))


    def get_points_from_formatted(self, mark:str) -> int:
        num_mark = 0
        if ":" in mark:
            split_mark = mark.split(":")
            if len(split_mark) == 2:
                num_mark = int(split_mark[0]) * 60 + float(split_mark[1])
            elif len(split_mark) == 3:
                num_mark = int(split_mark[0]) * 3600 + int(split_mark[1]) * 60 + float(split_mark[2])
        else:
            num_mark = float(mark)
        return self.get_points(num_mark)








class IaafConverter:

    def __init__(self):
        self.tables: Dict[str, IaafTableValue] = dict()

        with open('assets/conversion.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Get the values from the current row
                event = row['event']
                sex = row['sex']
                a = float(row['a'])
                b = float(row['b'])
                c = float(row['c'])
                time = True if row['time'] == 'true' else False
                integer = True if row['integer'] == 'true' else False
                name = str(sex).upper() + "-" + str(event)

                self.tables[name] = IaafTableValue(a, b, c, time, integer)


    def get_points(self, event:str, mark:str) -> int:
        if event in self.tables:
            return self.tables[event].get_points_from_formatted(mark)
        else:
            print_err("ERROR: " + event + " is not a valid event")


    def get_mark(self, event:str, points:int) -> str:
        if event in self.tables:
            return self.tables[event].get_formatted_mark(points)
        else:
            print_err("ERROR: " + event + " is not a valid event")


    def type_string(self) -> str:
        return "world_athletics_converter"



    def view(self, vars=None) -> str:
        buildstring = ""
        if vars is None:
            for event in self.tables.keys():
                buildstring += event + "\n"
        else:
            if vars[0] in self.tables.keys():
                buildstring += vars[0] + ":\n"
                buildstring += str(1) + " : " + self.get_mark(vars[0], 1) + "\n"
                for i in range(50, 1501, 50):
                    buildstring += str(i) + " : " + self.get_mark(vars[0], i) + "\n"
        return buildstring


    def help(self) -> str:
        build_str = ""
        build_str += Fore.LIGHTBLUE_EX
        build_str += "WORLD ATHLETICS COVERSION TABLES:\n"
        build_str += "The world athletics conversion tables provide a way for track and field events\n"
        build_str += "to be compared across both events and genders using a points system.\n"
        build_str += "From any mark in a given event one can get a point value, and from any\n"
        build_str += "point value one can get a mark for any event.\n"
        build_str += "* all measurements of length/height are in meters\n\n"
        build_str += "VIEW ALL AVAILABLE EVENTS:\n" + Fore.LIGHTGREEN_EX + "wa v" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "INSPECT A SPECIFIC EVENT:\n" + Fore.LIGHTGREEN_EX + "wa v [event]" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "GET POINTS FROM MARK:\n" + Fore.LIGHTGREEN_EX + "wa points [event] [mark]" \
                     + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "GET MARK FROM POINTS:\n" + Fore.LIGHTGREEN_EX + "wa mark [event] [points]" \
                     + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "GET EQUIVALENT MARK IN ALL OTHER EVENTS:\n" + Fore.LIGHTGREEN_EX + "wa spread [event] [mark]" \
                     + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "CONVERT A MARK FROM ONE EVENT TO ANOTHER:\n" + Fore.LIGHTGREEN_EX \
                     + "wa convert [event-1] [mark-in-event-1] [event-2]\n"
        build_str += Fore.RESET
        return build_str



    def handle(self, command:list):
        if len(command) < 2:
            return

        if command[1] == VIEW and len(command) > 2:
            print(self.view(vars=command[2:]))

        elif command[1] == VIEW:
            print(self.view())

        elif command[1] == MARK:
            if len(command) < 4:
                print_err("ERROR: mark command requires and event name and points value")
            else:
                try:
                    points = int(command[3])
                    print(self.get_mark(command[2], points))
                except:
                    print_err("ERROR: " + command[3] + " is not a valid points value")

        elif command[1] == POINTS:
            if len(command) < 4:
                print_err("ERROR: points command requires and event name and a mark value")
            else:
                try:
                    print(self.get_points(command[2], command[3]))
                except:
                    print_err("ERROR: " + command[3] + " is not a valid mark for the " + command[2])


        elif command[1] == SPREAD:
            if len(command) < 4:
                print_err("ERROR: spread command requires an event and a mark")
            else:
                try:
                    points = self.get_points(command[2], command[3])
                    for event in self.tables.keys():
                        print(event + ": " + self.tables[event].get_formatted_mark(points))

                except:
                    print_err("ERROR: " + command[3] + " is not a valid mark for the " + command[2])


        elif command[1] == CONVERT:
            if len(command) < 5:
                print_err("ERROR: convert command requires an event, a mark, and another event")
            else:
                if command[2] not in self.tables.keys() or command[4] not in self.tables.keys():
                    print_err("ERROR: " + command[2] + " and " + command[4] + " must be valid events")
                else:
                    try:
                        points = self.get_points(command[2], command[3])
                        print(self.tables[command[4]].get_formatted_mark(points))
                    except:
                        print_err("ERROR: " + command[3] + " is not a valid mark for the " + command[2])

        elif command[1] == HELP:
            print(self.help())


        else:
            print_err("ERROR: unknown world athletics conversion command: " + command[1])
