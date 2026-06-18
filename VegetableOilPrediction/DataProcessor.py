import os
import math
import pandas as pd
import numpy as np

def outputForm(formList: list, fileName: str, targetColumn) -> None:
    with open(f"{fileName}.txt", "w") as file:
        file.writelines(f"\t{targetColumn}\n")
        for count, each in enumerate(formList):
            file.writelines(str(count) + "\t" + str(each) + "\n")

class DataProcessor:
    def __init__(self, file_path: str, target_columns: list, asset_columns: list, autoFill: str = "None"):
        """
        Constructor: Initializes configuration and runs all processing logic immediately.
        """
        # Save original lists to instance variables for their respective getters
        self._target_columns = target_columns
        self._asset_columns = asset_columns
        
        # --- Your Original Processing Logic (Executed on Initialization) ---
        df = pd.read_csv(file_path)

        if(not set(self._asset_columns).issubset(set(self._target_columns))):
            raise Exception("Target Columns has to contain Asset Columns")

        for col in self._target_columns:
            if col not in df.columns:
                raise Exception("Parameter in Target Columns does not exist")

        # Renamed X to DataList as requested
        DataList = df[self._target_columns].values

        # create a dictionary matching column position and name
        columnMatches = {}
        for count, each in enumerate(self._target_columns):
            columnMatches[each] = count

        # detect which row has real actual number
        maxIndex = []
        for each in self._asset_columns:
            maxIndex.append(df[each].first_valid_index())
        
        # Save starting row to an instance variable for its getter
        self._starting_row = max(maxIndex)

        # print(self._starting_row, DataList[self._starting_row][0])
        # output the form in to a file since it is too big for direct print
        # outputForm(DataList, "FormDisplay", self._target_columns)

        # fill the later NaN slot with the same previous occured number
        if autoFill == "Repeat":
            lastObject = [DataList[self._starting_row][val] for _, val in columnMatches.items()]

            for count, each in enumerate(DataList[self._starting_row:], start=self._starting_row):
                for colName in self._asset_columns:
                    currentCol = columnMatches[colName]
                    if math.isnan(each[currentCol]):
                        DataList[count][currentCol] = lastObject[currentCol]
                    else:
                        lastObject[currentCol] = each[currentCol]
        elif autoFill == "None":
            pass
        else:
            raise Exception("Auto Fill String format not correct.")
            
        # outputForm(DataList, "UpdatedFrom", self._target_columns)
        # --- Your Original Processing Logic Ends Here ---

        # Slice DataList from the starting row and keep it as a NumPy array
        self._final_array = DataList[self._starting_row:]

    # --- Getters ---

    def get_final_list(self) -> np.ndarray:
        """Returns the final processed data as a NumPy ndarray starting from the first valid row."""
        return self._final_array

    def get_starting_row(self) -> int:
        """Returns the index of the row where real numbers actually start."""
        return self._starting_row

    def get_target_columns(self) -> list:
        """Returns the original target columns list."""
        return self._target_columns

    def get_asset_columns(self) -> list:
        """Returns the original asset columns list."""
        return self._asset_columns
    
    def get_starting_date(self) -> str:
        """Returns the starting data"""
        return self.get_final_list()[0][0]