from colorama import init, Fore, Back, Style
import pandas as pd
import matplotlib.pyplot as plt


STATS = "stats"
BOXPLOT = "boxplot"
HISTOGRAM = "hist"
COUNTS = "counts"
SCATTER = "scatter"

VIEW = "v"
GRAPH = "graph"
HELP = "help"



# used to print error messages
def print_err(text):
    print(Fore.RED + text)



# 1-variable stats on a whole column
def get_series_stats(column: pd.Series, settings) -> str:
    build_string = ""


    try:
        round_to = settings.get("round_to")
    except:
        print_err("ERROR: round_to needs to have an integer as its setting, defaulting to 4")
        round_to = 4

    # Type
    build_string += "TYPE: " + str(column.dtype) + "\n"

    # Count
    build_string += "LENGTH: " + str(len(column)) + "\n"

    # Sum
    build_string += "SUM: " + str(round(column.sum(), round_to)) + "\n"

    # Average (Mean)
    build_string += "MEAN: " + str(round(column.mean(), round_to)) + "\n"

    # Median
    build_string += "MEDIAN: " + str(round(column.median(), round_to)) + "\n"

    # Mode
    build_string += "MODE: "
    modes = column.mode()
    if len(modes) <= 10:
        for mode in modes:
            build_string += str(round(mode, round_to)) + ", "
        build_string = build_string[:-2]
    else:
        build_string += "more than 10 modes"
    build_string += "\n"

    # Minimum
    build_string += "MIN: " + str(round(column.min(), round_to)) + "\n"

    # Maximum
    build_string += "MAX: " + str(round(column.max(), round_to)) + "\n"

    # Standard dev
    build_string += "POPULATION STD DEV: " + str(round(column.std(ddof=0), round_to)) + "\n"

    # Sample standard dev
    build_string += "SAMPLE STD DEV: " + str(round(column.std(ddof=1), round_to)) + "\n"

    # Sample standard dev
    build_string += "NUM NAN VALUES: " + str(column.isna().sum()) + "\n"

    filled_column = column.fillna(0)

    build_string += "MEAN (NAN = 0): " + str(round(filled_column.mean(), round_to)) + "\n"

    build_string += "MEDIAN (NAN = 0): " + str(round(filled_column.median(), round_to)) + "\n"


    # Percentiles (5% increment)
    build_string += "\nPERCENTILES:\n"
    increment = .05
    end = .951
    q = increment
    while q < end:
        build_string += str(round(q * 100)) + "%: " + str(round(column.quantile(q), round_to)) + "\n"
        q += increment

    return build_string



# box and whisker plot
def series_boxplot(column: pd.Series):
    plt.boxplot(column)
    plt.title(str(column.name))
    plt.show()


# histogram of a single series
def series_hist(column: pd.Series, bins=10):
    plt.hist(column, bins=bins)
    plt.title(str(column.name))
    plt.show()


# scatter of a single series over the index, works great for columns in chronological order
def series_scatter(column: pd.Series):
    plt.scatter(column.index, column)
    plt.title(str(column.name))
    plt.show()






# ===========================================
#                 DATAFRAME
# ===========================================
class Dataframe:
    """
    Main data structure for a pandas dataframe
    """

    def __init__(self, csv_name: str, memory_bank, delimeter=None):
        self.settings = memory_bank.variables["settings"]
        path = memory_bank.variables["base"].cwd
        path = path.replace("~", memory_bank.variables["base"].base)
        path += "/" + csv_name

        if delimeter is None:
            self.df = pd.read_csv(path)
        elif delimeter == "whitespace":
            self.df = pd.read_csv(path, delim_whitespace=True)
        else:
            self.df = pd.read_csv(path, sep=delimeter)


        # Remove all spaces from names
        renames = dict()
        for column in self.df.columns:
            new_name = column.replace(" ", "_")
            if column != new_name:
                renames[column] = new_name

        if len(renames) > 0:
            self.df = self.df.rename(columns=renames)


    def get_all_column_names(self) -> list:
        return list(self.df.columns)


    def column_exists(self, column_name: str) -> bool:
        return column_name in self.get_all_column_names()


    def get_column(self, column_key: str) -> pd.Series:
        if not self.column_exists(column_key):
            print_err("ERROR: Column " + column_key + " does not exist")
            return None
        return self.df[column_key]


    def get_subsection(self, subsection: str) -> pd.Series:
        return self.get_column(subsection)


    def type_string(self) -> str:
        return "dataframe [" + str(len(self.get_all_column_names())) + " columns, " + str(len(self.df.index)) + " rows]"


    def view(self, vars=None) -> str:
        if vars is None:
            return str(self.df.head())
        else:
            try:
                num = int(vars[0])
                return str(self.df.head(num))
            except:
                print_err("ERROR: additional variable for viewing a dataframe must be an integer")
                return None



    def view_subsection(self, subsection, vars=None) -> str:

        # If asking to view column names
        if subsection == "columns":
            build_string = ""
            for col in self.get_all_column_names():
                build_string += col + "\n"
            return build_string[:-1]

        # If invalid item after . then throw error
        elif subsection not in self.get_all_column_names():
            print_err("ERROR: " + subsection + " is not a column in the dataframe")
            return None

        # Asking to view an individual column
        else:
            # No vars just display whole
            if vars is None:
                return str(self.df[subsection])

            # Check for stats
            elif vars[0] == STATS:
                if str(self.df[subsection].dtype) == "object":
                    print_err("ERROR: cannot get stats on series of type object")
                else:
                    return get_series_stats(self.df[subsection], settings=self.settings)

            # Graph a box and whiskers plot
            elif vars[0] == BOXPLOT:
                if str(self.df[subsection].dtype) == "object":
                    print_err("ERROR: cannot view boxplot on series of type object")
                else:
                    series_boxplot(self.df[subsection])
                    return "boxplot"

            # Graph a histogram
            elif vars[0] == HISTOGRAM:
                if str(self.df[subsection].dtype) == "object":
                    print_err("ERROR: cannot view histogram on series of type object")
                else:
                    bins = 10
                    if len(vars) > 1:
                        try:
                            bins = int(vars[1])
                        except:
                            print_err("ERROR: " + str(vars[1]) + " is not a valid number, using 10 bins")
                            bins = 10
                    series_hist(self.df[subsection], bins=bins)
                    return "histogram"

            # View counts
            elif vars[0] == COUNTS:
                all_counts = self.df[subsection].value_counts()
                return str(all_counts)

            # View a scatter plot
            elif vars[0] == SCATTER:
                if str(self.df[subsection].dtype) == "object":
                    print_err("ERROR: cannot view scatter on series of type object")
                else:
                    series_scatter(self.df[subsection])
                    return "scatter plot"

    def help(self) -> str:
        build_str = ""
        build_str += Fore.LIGHTBLUE_EX
        build_str += "DATAFRAME TOOL:\n"
        build_str += "This tool allows users to pin csvs as dataframes and perform\n"
        build_str += "analysis on them.\n\n"
        build_str += "VIEW ALL COLUMN HEADERS:\n" + Fore.LIGHTGREEN_EX + "[name] v columns" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW HEAD OF DATAFRAME:\n" + Fore.LIGHTGREEN_EX + "[name] v" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW COLUMN:\n" + Fore.LIGHTGREEN_EX + "[name] v [column]" + Fore.LIGHTBLUE_EX + "\n\n"
        build_str += "VIEW COLUMN STATS:\n" + Fore.LIGHTGREEN_EX + "[name] v [column] stats" + Fore.LIGHTBLUE_EX + "\n\n"

        build_str += "VIEW COLUMN AS HISTOGRAM:\n"
        build_str += Fore.LIGHTGREEN_EX + "[name] v [column] hist " + Fore.LIGHTBLACK_EX + \
                     "{opt:n}\n\n" + Fore.LIGHTBLUE_EX

        build_str += "VIEW COLUMN AS SCATTER PLOT:\n" + Fore.LIGHTGREEN_EX + "[name] v [column] scatter" \
                     + Fore.LIGHTBLUE_EX + "\n\n"

        build_str += "VIEW COLUMN AS BOX PLOT:\n" + Fore.LIGHTGREEN_EX + "[name] v [column] boxplot" \
                     + Fore.LIGHTBLUE_EX + "\n\n"

        build_str += "GRAPH RELATIONSHIP BETWEEN 2 COLUMNS:\n" + Fore.LIGHTGREEN_EX + \
                     "[name] graph [x-column] [y-column]" \
                     + Fore.LIGHTBLUE_EX + "\n\n"

        build_str += Fore.RESET
        return build_str




    def handle(self, command: list):
        if len(command) < 2:
            return

        if command[1] == VIEW and len(command) > 3:
            print(self.view_subsection(subsection=command[2], vars=command[3:]))
        elif command[1] == VIEW and len(command) > 2:
            print(self.view_subsection(subsection=command[2], vars=None))
        elif command[1] == VIEW:
            print(self.view())
        elif command[1] == HELP:
            print(self.help())
        elif command[1] == GRAPH:
            if command[2] not in self.get_all_column_names() or command[3] not in self.get_all_column_names():
                print_err("ERROR: " + command[2] + " and " + command[3] + " must be valid column names")
            else:
                plt.scatter(self.df[command[2]], self.df[command[3]])
                plt.title(str(command[2] + " vs " + command[3]))
                plt.show()

        else:
            print_err("ERROR: unknown dataframe command: " + command[1])
