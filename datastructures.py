
from colorama import init, Fore, Back, Style
import pandas as pd
import file_system
import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like
from sklearn.linear_model import LinearRegression


# initialize colorama
init(convert=True, autoreset=True)



# ===========================================
#                 SETTINGS
# ===========================================
class Settings:
    """
    Settings:

    base: the base file folder for files to be stored
    """
    def __init__(self):
        self.settings = dict()
        settings_file = open("settings.txt", "r")
        for line in settings_file:
            subline = line.split(">")
            if len(subline) == 2:
                value = subline[1]
                if value.endswith("\n"):
                    value = value[:-1]
                self.settings[subline[0]] = value

    def get_setting(self, key: str) -> str:
        if key in self.settings.keys():
            return self.settings[key]
        else:
            print_err("ERROR: " + key + " is not a valid setting")


# Instantiate a global settings instance
GLOBAL_SETTINGS = Settings()



def print_err(text):
    print(Fore.RED + text)




# ===========================================
#            GLOBAL FUNCTIONS
# ===========================================


# 1-variable stats on a whole column
def get_series_stats(column: pd.Series) -> str:
    build_string = ""


    try:
        round_to = int(GLOBAL_SETTINGS.get_setting("round_to"))
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
    plt.title = str(column.name)
    plt.show()


# histogram of a single series
def series_hist(column: pd.Series, bins=10):
    plt.hist(column, bins=bins)
    plt.title = str(column.name)
    plt.show()


# scatter of a single series over the index, works great for columns in chronological order
def series_scatter(column: pd.Series):
    plt.scatter(column.index, column)
    plt.title = str(column.name)
    plt.show()





def binarize_lambda(row, column_name,value) -> int:
    if row[column_name] == value:
        return 1
    else:
        return 0







# ===========================================
#                MEMORY BANK
# ===========================================
class MemoryBank:
    """
    Class that defines all storage of variables
    """

    def __init__(self):
        self.variables = dict()
        self.variables["mem"] = self
        self.variables["base"] = file_system.FolderStructure(GLOBAL_SETTINGS.get_setting("base"))


    def var_exists(self, key: str) -> bool:
        return key in self.variables.keys()


    def get_var(self, key: str):
        return self.variables[key]


    def type_string(self) -> str:
        return "memory_bank"


    def add_var(self, key: str, value):
        if self.var_exists(key):
            print_err("ERROR: " + key + " is a taken variable name in memory")
        else:
            self.variables[key] = value


    def get_subsection(self, subsection: str):
        if self.var_exists(subsection):
            return self.get_var(subsection)
        else:
            print_err("ERROR: " + subsection + " does not exist")
            return None


    def view(self, vars=None) -> str:
        build_string = ""
        for var in self.variables.keys():
            build_string += var + " : " + self.variables[var].type_string() + "\n"
        return build_string


    def view_subsection(self, subsection, vars=None) -> str:
        if subsection in self.variables.keys():
            return self.variables[subsection].view(vars=vars)
        else:
            print_err("ERROR: " + subsection + " does not exist in memory")


    def cd(self, path:str):
        self.variables["base"].cd(path)


    def dir(self) -> str:
        return self.variables["base"].dir()


    def ls(self):
        self.variables["base"].ls()


    def mkdir(self, dir_name:str):
        self.variables["base"].mkdir(dir_name)

    def set(self, name: str, value, vars=None):
        print_err("ERROR: memory_bank does not implement setting variables")









STATS = "stats"
BOXPLOT = "boxplot"
HISTOGRAM = "hist"
COUNTS = "counts"
SCATTER = "scatter"







# ===========================================
#                 DATAFRAME
# ===========================================
class Dataframe:
    """
    Main data structure for a pandas dataframe
    """

    def __init__(self, csv_name: str, memory_bank:MemoryBank):
        path = memory_bank.variables["base"].cwd
        path = path.replace("~", memory_bank.variables["base"].base)
        path += "/" + csv_name
        self.df = pd.read_csv(path)


    def get_all_column_names(self) -> list:
        return list(self.df.columns)


    def get_column(self, column_key: str) -> pd.Series:
        if column_key not in self.df.columns:
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
                    return get_series_stats(self.df[subsection])

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



    def set(self, name: str, value, vars=None):
        print_err("ERROR: dataframe does not implement setting variables")



    def numericize(self, column_name: str, vars=None):
        # Ger the column
        column: pd.Series = self.get_column(column_name)

        # Error if column doesn't exist
        if column is None:
            print_err("ERROR: " + column_name + " is not a column in this dataframe")
            return
        # Error is column is already numerical
        elif str(column.dtype) != "object":
            print_err("ERROR: " + column_name + " is not an object column")
            return

        # Past error catching, now numericize the column
        all_counts = column.value_counts()

        for element in all_counts.keys():
            header = column_name + "_is_" + element
            self.df[header] = self.df.apply(lambda row: binarize_lambda(row, column_name, element), axis=1)













# ===========================================
#                BASIC PLOT
# ===========================================
class BasicPlot:
    """
    Data structure for a 2d matplotlib plot
    """

    def __init__(self):

        self.variables = {
            "x": None,
            "y": None,
            "alpha": 1.0,
            "xlabel": None,
            "ylabel": None,
            "title": None,
            "regression_line": False,
            "color": "blue",
            "size": 4
        }



    def type_string(self) -> str:
        return "basic_plot"


    def set(self, name: str, value, vars=None):

        if name == "x":
            if type(value) == pd.Series and str(value.dtype) != "object":
                self.variables["x"] = value
            else:
                print_err("ERROR: x value must be a column or series and cannot be of type object")

        elif name == "y":
            if type(value) == pd.Series and str(value.dtype) != "object":
                self.variables["y"] = value
            else:
                print_err("ERROR: y value must be a column or series and cannot be of type object")

        # setting alpha value
        elif name == "alpha":
            try:
                num = float(value)
                self.variables["alpha"] = num
            except:
                print_err("ERROR: " + str(value) + " is not a valid float")

        # setting color
        elif name == "color":
            if not is_color_like(value):
                print_err("ERROR: " + str(value) + " is not a valid color")
            else:
                self.variables["color"] = value

        # setting size
        elif name == "size":
            try:
                num = int(value)
                if num > 0:
                    self.variables["size"] = num
                else:
                    print_err("ERROR: " + str(value) + " is not a positive integer")
            except:
                print_err("ERROR: " + str(value) + " is not a valid integer")

        # If asking for a regression line
        elif name == "regression_line":
            if value.lower() == "true" or value.lower() == "t":
                self.variables["regression_line"] = True
            elif value.lower() == "false" or value.lower() == "f":
                self.variables["regression_line"] = False
            else:
                print_err("ERROR: " + str(value) + " is not a valid boolean -> (true, false, t, f)")

        # Catch all for other string variables
        elif name in self.variables:
            self.variables[name] = value

        # Unknown variable
        else:
            print_err("ERROR: " + name + " is not a known variable in basic_plot")




    def get_subsection(self, subsection: str):
        if subsection in self.variables.keys():
            return self.variables[subsection]
        else:
            print_err("ERROR: " + subsection + " is not a known variable in basic_plot")
            return None




    def view(self, vars=None) -> str:
        x = self.variables["x"]
        y = self.variables["y"]
        alpha = self.variables["alpha"]
        size = self.variables["size"]
        color = self.variables["color"]
        xlabel = self.variables["xlabel"]
        ylabel = self.variables["ylabel"]
        title = self.variables["title"]
        regression_line = self.variables["regression_line"]

        if vars is None:
            if len(x) != len(y):
                print_err("ERROR: x and y are not the same length")
            else:
                x_label = xlabel if xlabel is not None else str(x.name)
                y_label = ylabel if ylabel is not None else str(y.name)
                title = title if title is not None else x_label + " vs " + y_label

                plt.scatter(x, y, alpha=alpha, s=size, c=color)
                plt.title(title)
                plt.xlabel(x_label)
                plt.ylabel(y_label)

                if regression_line:
                    X = x.values.reshape(-1, 1)
                    Y = y.values.reshape(-1, 1)
                    linear_regressor = LinearRegression()
                    linear_regressor.fit(X, Y)
                    Y_pred = linear_regressor.predict(X)
                    plt.plot(X, Y_pred, color='red')

                # Show final graph
                plt.show()

            return self.type_string()

        # If there are vars
        else:
            # if looking for all variables
            if vars[0] == "stats":
                build_string = ""
                for variable in self.variables:
                    build_string += variable + ": "

                    # if its x or y just show name rather than whole list
                    if variable == "x" or variable == "y":
                        if self.variables[variable] is not None:
                            build_string += str(self.variables[variable].name) + \
                                            " [" + str(len(self.variables[variable])) + " items]"
                        else:
                            build_string += "None"

                    # for rest of variables show literal value
                    else:
                        build_string += str(self.variables[variable])
                    build_string += "\n"
                return build_string


            # check if asking for specific variable
            elif vars[0] in self.variables.keys():
                if vars[0] == "x" or vars[0] == "y":
                    return str(self.variables[vars[0]])
                else:
                    return vars[0] + ": " + str(self.variables[vars[0]])


            # if invalid vars, then view without vars
            else:
                return self.view(vars=None)











