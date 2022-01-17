
from colorama import init, Fore, Back, Style
import pandas as pd
import file_system
import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like
from sklearn.metrics import confusion_matrix
import numpy as np


# import ML models
from sklearn.linear_model import LinearRegression, SGDClassifier, SGDRegressor
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.svm import SVR, SVC
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier


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











# ===========================================
#            GLOBAL FUNCTIONS
# ===========================================


# used to print error messages
def print_err(text):
    print(Fore.RED + text)



def msg_box(msg, indent=1, width=None, title=None):
    """
    put text in message-box with optional title.
    """
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    return box




def textual_confusion_matrix(matrix: np.ndarray, labels):
    box = [[]]
    col_widths = [0]
    size = matrix.shape[0]
    build_string = ""
    sum = 0

    for i in range(size):
        box.append([])
        col_widths.append(0)


    box[0].append(" ")
    for i in range(len(labels)):
        item = str(labels[i]) + "_pred"
        box[0].append(item)
        if len(item) > col_widths[i + 1]:
            col_widths[i + 1] = len(item)

    for row in range(size):
        item = str(labels[row]) + "_true"
        box[row + 1].append(item)
        if len(item) > col_widths[0]:
            col_widths[0] = len(item)

        for col in range(size):
            item = matrix[row, col]
            box[row + 1].append(item)
            if len(str(item)) > col_widths[col]:
                col_widths[col] = len(item)


    for i in range(len(col_widths)):
        sum += col_widths[i]
    sum += 3 * (len(col_widths) - 1)


    for row in range(len(box)):
        for col in range(len(box[row])):
            item = str(box[row][col])
            build_string += item
            spaces = col_widths[col] - len(item)
            build_string += " " * spaces
            if col < len(box[row]) - 1:
                build_string += " | "

        if row < len(box) - 1:
            build_string += "\n"
            build_string += "-" * sum
            build_string += "\n"

    return msg_box(build_string)







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




# Helper function used in numericizing columns from objects to a series of binary columns
def binarize_lambda(row, column_name, value) -> int:
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

    def __init__(self, csv_name: str, memory_bank:MemoryBank, delimeter=None):
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



    def classify(self, column_name: str, vars=None):
        column: pd.Series = self.get_column(column_name)

        # Error if column doesn't exist
        if column is None:
            print_err("ERROR: " + column_name + " is not a column in this dataframe")
            return
        # Error is column is already numerical
        elif str(column.dtype) != "object":
            print_err("ERROR: " + column_name + " is not an object column")
            return

        # Past error catching, now classify the column
        all_counts = column.value_counts()

        header = column_name + "_classified"
        self.df[header] = pd.factorize(self.df[column_name])[0]











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
            if x is None or y is None:
                print_err("ERROR: x and y must both be defined as a series")
                return
            elif len(x) != len(y):
                print_err("ERROR: x and y are not the same length")
                return
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



    def view_subsection(self, subsection, vars=None) -> str:
        if subsection in self.variables:
            return str(self.variables[subsection])
        else:
            print_err("ERROR: " + subsection + " is not a valid basic_plot variable")


















##############################################################################################
#                              [   MACHINE LEARNING SECTION   ]
##############################################################################################



# ===========================================
#                    MODEL
# ===========================================
class Model:

    def __init__(self, dataframe: Dataframe):
        # Whether classifier or regressor
        self.model_type = "regressor"

        # Dataframe used for all data
        self.df: Dataframe = dataframe

        # Mutable variables
        self.inputs: list = []
        self.outputs: list = []
        self.fitted: bool = False
        self.model = None
        self.test_set_ratio = 0.15

        self.type = "mlp"

        self.TYPES = [
            "mlp",
            "svm",
            "decision_tree",
            "linear"
        ]


        # MLP variables
        self.hidden = [64]
        self.solver = "lbfgs"
        self.learning_rate = "constant"
        self.lr_init = 0.001

        self.SOLVERS = [
            "lbfgs",
            "adam",
            "sgd"
        ]

        self.LEARNING_RATES = [
            "constant",
            "invscaling",
            "adaptive"
        ]



        self.diff_frame = None
        self.abs_diff_frame = None

        self.correctness = None
        self.confusion_matrix = None

        self.class_labels = None
        self.labeled = False

        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.y_pred = None




    def add_input(self, column_name: str):
        if column_name == "**":
            for each_col in self.df.get_all_column_names():
                if str(self.df.get_column(each_col).dtype) != "object":
                    self.inputs.append(each_col)
                    self.fitted = False

        elif not self.df.column_exists(column_name):
            print_err("ERROR: " + column_name + " does not exist in the dataframe")

        elif str(self.df.get_column(column_name).dtype) == "object":
            print_err("ERROR: columns must be numeric, type object is not allowed in ML models")

        elif column_name in self.outputs:
            print_err("ERROR: " + column_name + " is an output and cannot be an input")

        else:
            self.inputs.append(column_name)
            self.fitted = False



    def remove_input(self, column_name: str):
        if column_name in self.inputs:
            self.inputs.remove(column_name)
            self.fitted = False
        else:
            print_err("ERROR: " + column_name + " is not in the inputs")



    def add_output(self, column_name: str):
        if len(self.outputs) > 0:
            print_err("ERROR: model only supports one output column")

        elif not self.df.column_exists(column_name):
            print_err("ERROR: " + column_name + " does not exist in the dataframe")

        elif str(self.df.get_column(column_name).dtype) == "object":
            print_err("ERROR: columns must be numeric, type object is not allowed in ML models")

        elif column_name in self.inputs:
            print_err("ERROR: " + column_name + " is an input and cannot be an output")

        else:
            self.outputs.append(column_name)
            if column_name.endswith("_classified"):
                unclassified = column_name[:-11]
                if self.df.column_exists(unclassified):
                    codes, uniques = pd.factorize(self.df.get_column(unclassified))
                    self.class_labels = uniques
                    self.labeled = True
            else:
                codes, uniques = pd.factorize(self.df.get_column(column_name))
                self.class_labels = uniques
                self.labeled = False
            self.fitted = False



    def remove_output(self, column_name: str):
        if column_name in self.outputs:
            self.outputs.remove(column_name)
            self.fitted = False
        else:
            print_err("ERROR: " + column_name + " is not in the outputs")



    def view(self, vars=None) -> str:

        # If vars is none then just display stats
        if vars is None:
            # Inputs
            build_string = "INPUTS:\n"
            for col in self.inputs:
                build_string += "  " + col + "\n"

            # Outputs
            build_string += "\nOUTPUTS:\n"
            for col in self.outputs:
                build_string += "  " + col + "\n"
            build_string += "\n"

            # Fitted
            build_string += "fitted: " + str(self.fitted) + "\n"

            # Test set ratio
            build_string += "test_set_ratio: " + str(self.test_set_ratio) + "\n"

            # Type
            build_string += "type: " + self.type + "\n\n"



            # Vars for MLP NNet
            if self.type == "mlp":

                # Hidden
                build_string += "hidden: " + str(self.hidden) + "\n"

                # Solver
                build_string += "solver: " + str(self.solver) + "\n"

                # Learning Rate
                build_string += "learning_rate: " + str(self.learning_rate) + "\n"

                # Learning Rate Init
                build_string += "lr_init: " + str(self.lr_init) + "\n"

            return build_string




        # RESULTS for regressor
        elif vars[0] == "results" and self.model_type == "regressor":
            if not self.fitted:
                print_err("ERROR: regressor must be fitted to view results")
                return

            build_string = "PREDICTED VS ACTUAL:\n"
            build_string += "==========================\n"
            build_string += get_series_stats(self.diff_frame)
            build_string += "\n\n\n"

            build_string += "ABSOLUTE VALUE OF PREDICTED VS ACTUAL:\n"
            build_string += "==========================\n"
            build_string += get_series_stats(self.abs_diff_frame)

            return build_string



        # RESULTS for classifier
        elif vars[0] == "results" and self.model_type == "classifier":
            if not self.fitted:
                print_err("ERROR: regressor must be fitted to view results")
                return

            build_string = "ACCURACY LIST (1 = correct, 0 = wrong):\n"
            build_string += "==========================\n"
            build_string += get_series_stats(self.correctness)
            build_string += "\n\n\n\n"

            build_string += "CONFUSION MATRIX:\n"
            build_string += "==========================\n"
            build_string += "\n\n"
            build_string += textual_confusion_matrix(self.confusion_matrix, self.class_labels)
            return build_string






        # EXAMPLES
        elif vars[0] == "examples":
            if not self.fitted:
                print_err("ERROR: regressor must be fitted to view examples")
                return

            build_string = ""
            num_examples = 10
            round_to = int(GLOBAL_SETTINGS.get_setting("round_to"))

            if len(vars) > 1:
                try:
                    num_examples = int(vars[1])
                except:
                    print_err("ERROR: " + vars[1] + " is not a valid integer, defaulting to 10.")


            # Make sure to not overflow beyond number of predictions
            if len(self.y_pred) < num_examples:
                num_examples = len(self.y_pred)

            # for each example
            for i in range(num_examples):
                index = self.y_test.index[i]

                build_string += "\n\n==========================\n"
                # show each input
                for input in self.inputs:
                    build_string += input + ": "
                    build_string += str(round(self.df.df.at[index, input], round_to)) + "\n"



                # show the output
                build_string += self.outputs[0] + ": "
                if self.model_type == "regressor" or not self.labeled:
                    build_string += str(round(self.df.df.at[index, self.outputs[0]], round_to)) + "\n"
                else:
                    label_index = self.df.df.at[index, self.outputs[0]]
                    build_string += str(self.class_labels[label_index]) + "\n"


                # show the predicted output
                build_string += self.outputs[0] + "_prediction: "
                if self.model_type == "regressor" or not self.labeled:
                    build_string += str(round(self.y_pred[i], round_to)) + "\n"
                else:
                    label_index = self.y_pred[i]
                    build_string += str(self.class_labels[label_index]) + "\n"


                build_string += "==========================\n"

            return build_string








    def view_subsection(self, subsection, vars=None) -> str:
        build_string = ""

        if subsection == "inputs":
            # Inputs
            build_string += "INPUTS:\n"
            for col in self.inputs:
                build_string += "  " + col + "\n"

        elif subsection == "inputs":
            build_string += "OUTPUTS:\n"
            for col in self.outputs:
                build_string += "  " + col + "\n"

        elif subsection == "fitted":
            build_string = str(self.fitted)

        elif subsection == "test_set_ratio":
            build_string = str(self.test_set_ratio)

        elif subsection == "type":
            build_string = str(self.type)

        elif subsection == "hidden":
            build_string = str(self.hidden)

        elif subsection == "solver":
            build_string = str(self.solver)

        elif subsection == "learning_rate":
            build_string = str(self.learning_rate)

        elif subsection == "lr_init":
            build_string = str(self.lr_init)

        else:
            print_err("ERROR: " + subsection + " is not a known regressor variable")






    # SET variable to a value
    def set(self, name: str, value, vars=None):

        if name == "model_type":
            if value == "regressor" or value == "classifier":
                self.model_type = value
            else:
                print_err("ERROR: " + value + " is not a valid model_type, must be classifier or regressor")

        # test_set_ratio
        elif name == "test_set_ratio":
            try:
                r = float(value)
                if r <= 0:
                    print_err("ERROR: test_set_ratio must be positive")
                    return
                self.test_set_ratio = r
            except:
                print_err("ERROR: test_set_ratio must be a positive float")


        # type
        elif name == "type":
            if value in self.TYPES:
                self.type = value
                self.fitted = False
            else:
                print_err("ERROR: " + value + " is an invalid type, must be in set: " + str(self.TYPES))


        # hidden
        elif name == "hidden":
            old_hidden = self.hidden

            try:
                hid = int(value)
                self.hidden = [hid]
            except:
                print_err("ERROR: " + value + " is not a valid integer")
                return

            if vars is not None:
                for element in vars:
                    try:
                        hid = int(element)
                        self.hidden.append(hid)
                    except:
                        print_err("ERROR: " + element + " is not a valid integer")
                        self.hidden = old_hidden
                        return
            self.fitted = False


        # solver
        elif name == "solver":
            if value in self.SOLVERS:
                self.solver = value
                self.fitted = False
            else:
                print_err("ERROR: " + value + " is an invalid solver, must be in set: " + str(self.SOLVERS))


        # learning_rate
        elif name == "learning_rate":
            if value in self.LEARNING_RATES:
                self.learning_rate = value
                self.fitted = False
            else:
                print_err("ERROR: " + value + " is an invalid learning_rate, must be in set: " + str(self.LEARNING_RATES))


        # lr_init (initial learning rate)
        elif name == "lr_init":
            try:
                lr = float(value)
                if lr < 0:
                    print_err("ERROR: lr_init must be positive")
                    return
                self.lr_init = lr
                self.fitted = False
            except:
                print_err("ERROR: lr_init must be a positive float")


        else:
            print_err("ERROR: " + name + " is not a known regressor variable")



    def get_subsection(self, subsection: str):
        print_err("ERROR: regressor does not implement getting subsections")



    def type_string(self):
        return "model [" + self.model_type + "][" + self.type + "]"




    def __create_difference_columns(self):
        self.diff_frame = []
        self.abs_diff_frame = []

        #print(self.y_test)
        #print(self.y_pred)

        for pi, ti in enumerate(self.y_test.index):
            test_val = self.y_test[ti]
            pred_val = self.y_pred[pi]

            self.diff_frame.append(pred_val - test_val)
            self.abs_diff_frame.append(abs(pred_val - test_val))

        self.diff_frame = pd.Series(self.diff_frame)
        self.abs_diff_frame = pd.Series(self.abs_diff_frame)



    def __create_classification_results(self):
        self.correctness = []

        for pi, ti in enumerate(self.y_test.index):
            test_val = self.y_test[ti]
            pred_val = self.y_pred[pi]
            self.correctness.append(1 if test_val == pred_val else 0)

        self.correctness = pd.Series(self.correctness)
        if self.labeled:
            self.confusion_matrix = confusion_matrix(self.y_test, self.y_pred)
        else:
            self.confusion_matrix = confusion_matrix(self.y_test, self.y_pred, labels=self.class_labels)





    def fit(self):
        if len(self.outputs) < 1:
            print_err("ERROR: output field is empty")
            return

        if len(self.inputs) < 1:
            print_err("ERROR: inputs are empty")
            return

                # Inputs and output values
        X = self.df.df[self.inputs]
        y = self.df.df[self.outputs[0]]

        # Train test split
        self.X_train, \
        self.X_test, \
        self.y_train, \
        self.y_test = train_test_split(X, y, test_size=self.test_set_ratio)


        # Models for regression
        if self.model_type == "regressor":
            # get the type
            if self.type == "mlp":
                # Initialize the model
                self.model = MLPRegressor(hidden_layer_sizes=self.hidden,
                                          activation=GLOBAL_SETTINGS.get_setting("activation"),
                                          solver=self.solver,
                                          alpha=float(GLOBAL_SETTINGS.get_setting("mlp_alpha")),
                                          learning_rate=self.learning_rate,
                                          learning_rate_init=self.lr_init)

            elif self.type == "svm":
                # Initialize the model
                self.model = SVR()

            elif self.type == "linear":
                self.model = LinearRegression()

            elif self.type == "decicion_tree":
                self.model = DecisionTreeRegressor()



        # Models for classification
        elif self.model_type == "classifier":
            # get the type
            if self.type == "mlp":
                # Initialize the model
                self.model = MLPClassifier(hidden_layer_sizes=self.hidden,
                                          activation=GLOBAL_SETTINGS.get_setting("activation"),
                                          solver=self.solver,
                                          alpha=float(GLOBAL_SETTINGS.get_setting("mlp_alpha")),
                                          learning_rate=self.learning_rate,
                                          learning_rate_init=self.lr_init)

            elif self.type == "svm":
                # Initialize the model
                self.model = SVC()

            elif self.type == "linear":
                print_err("ERROR: no linear classifier, change type to something else")

            elif self.type == "decicion_tree":
                self.model = DecisionTreeClassifier()


        self.model.fit(self.X_train, self.y_train)

        self.y_pred = self.model.predict(self.X_test)

        self.fitted = True

        # Fill results
        if self.model_type == "regressor":
            self.__create_difference_columns()
        elif self.model_type == "classifier":
            self.__create_classification_results()


















