from cryptography.fernet import Fernet
import pickle
from typing import Optional, List, Dict
from collections import OrderedDict
from tabulate import tabulate
import pandas as pd

VALUE_START = "> "
VALUE_DELIMETER = ":"
INT_TAG = " [int] "
INT_ARRAY_TAG = " [array[int]] "
FLOAT_ARRAY_TAG = " [array[float]] "
FLOAT_TAG = " [float] "
ENCRYPTED_TAG = " [encrypted] "


class DatafileValue:
    def __init__(self):
        self.info: str = ""
        self.name: str = ""
        self.is_encrypted: bool = False
        self.encrypted_value: Optional[str] = None
        self.tag: Optional[str] = None
        self.value = None


class Datafile:
    def __init__(self, filepath: str, key: Optional[str] = None):
        self.filepath = filepath
        self.values: Dict[str, DatafileValue] = OrderedDict()

        file = open(filepath, "r")
        lines = file.readlines()


        # if there is a key, initialize the cryptographer
        self.cryptographer: Optional[Fernet] = None
        if key is not None:
            try:
                keyfile = open(key, "rb")
                self.cryptographer = pickle.load(keyfile)
            except:
                print("could not load key")


        # Iterate through all the lines
        current_val = DatafileValue()
        for line in lines:

            # If this is a data line, then store the value
            if line.startswith(VALUE_START) and VALUE_DELIMETER in line:
                split = line.split(VALUE_DELIMETER)

                current_val.name = split[0].strip().split(" ")[-1]

                # Cast value to int
                if INT_TAG in split[0]:
                    try:
                        current_val.value = int(split[1])
                        current_val.tag = "int"
                    except:
                        print("Error, " + current_val.name + " is not an int.")
                        current_val.value = None

                # Cast value to float
                elif FLOAT_TAG in split[0]:
                    try:
                        current_val.value = float(split[1])
                        current_val.tag = "float"
                    except:
                        print("Error, " + current_val.name + " is not a float.")
                        current_val.value = None

                # get encrypted string
                elif ENCRYPTED_TAG in split[0]:
                    if self.cryptographer is not None:
                        current_val.encrypted_value = split[1].strip()
                        current_val.value = self.cryptographer.decrypt(bytes.fromhex(split[1].strip())).decode()
                        current_val.is_encrypted = True
                        current_val.tag = "encrypted"
                    else:
                        current_val.encrypted_value = split[1].strip()
                        current_val.value = split[1].strip()
                        current_val.is_encrypted = True
                        current_val.tag = "encrypted"

                # Store value as string
                else:
                    current_val.value = split[1].strip()

                self.values[current_val.name] = current_val
                current_val = DatafileValue()


            # Line of info
            elif len(line) > 1:
                current_val.info += line

        file.close()




    def view(self):
        names = []
        values = []
        tags = []
        for name in self.values.keys():
            names.append(name)

            values.append(str(self.values[name].value))

            if self.values[name].tag is not None:
                tags.append(self.values[name].tag)
            else:
                tags.append(" ")

        df = pd.DataFrame({'name': names, 'value': values, 'tag': tags})
        print(tabulate(df, headers='keys', tablefmt='fancy_grid'))




    def view_specific(self, name:str):
        if name not in self.values.keys():
            print("NO ENTRY")
            return
        if self.values[name].info is not None:
            print(self.values[name].info)
        if self.values[name].is_encrypted:
            print("[encrypted]")
        print(self.values[name].name + ": " + str(self.values[name].value))



    def add(self, name:str, value, is_encrypted:bool = False, info:Optional[str] = None, tag:Optional[str] = None):
        new_data = DatafileValue()
        new_data.name = name
        new_data.value = value
        new_data.is_encrypted = is_encrypted
        new_data.info = info
        new_data.tag = tag

        if new_data.is_encrypted and self.cryptographer is not None:
            new_data.encrypted_value = self.cryptographer.encrypt(new_data.value.encode()).hex()

        self.values[new_data.name] = new_data



    def delete(self, name: str):
        if name in self.values.keys():
            del self.values[name]



    def save(self):
        file = open(self.filepath, "w")

        for name in self.values.keys():
            if self.values[name].info is not None:
                file.write(self.values[name].info.rstrip() + "\n")
            buildstr = "> "
            if self.values[name].tag is not None:
                buildstr += "[" + self.values[name].tag + "] "
            buildstr += name + ": "
            if self.values[name].is_encrypted:
                buildstr += str(self.values[name].encrypted_value)
            else:
                buildstr += str(self.values[name].value)

            file.write(buildstr + "\n\n")

        file.close()

