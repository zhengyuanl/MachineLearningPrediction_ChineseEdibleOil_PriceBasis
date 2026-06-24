import os
import pandas as pd
import numpy as np

def outputForm(formList: list, fileName: str, targetColumn) -> None:
    # Kept intact as requested
    with open(f"{fileName}.txt", "w") as file:
        file.writelines(f"\t{targetColumn}\n")
        for count, each in enumerate(formList):
            file.writelines(str(count) + "\t" + str(each) + "\n")


class DataProcessor:
    def __init__(self, file_path: str, target_columns: list, asset_columns: list, autoFill: str = "None"):
        self._target_columns = target_columns
        self._asset_columns = asset_columns
        
        # 1. Read only the columns you actually care about
        df = pd.read_csv(file_path)

        # 2. Robust validation checks
        if not set(self._asset_columns).issubset(set(self._target_columns)):
            raise Exception("Target Columns has to contain Asset Columns")

        if not set(self._target_columns).issubset(set(df.columns)):
            raise Exception("Parameter in Target Columns does not exist")

        # 3. Dynamic slice: Find where valid data starts across ALL asset columns
        max_index = max([df[col].first_valid_index() for col in self._asset_columns])
        self._starting_row = max_index

        # Slice the dataframe from the starting row onwards and grab target columns
        df_sliced = df.loc[self._starting_row:, self._target_columns].copy()

        # 4. Elastic Autofill using Pandas native Vectorization
        if autoFill == "Repeat":
            # Only forward-fill the asset columns specifically
            df_sliced[self._asset_columns] = df_sliced[self._asset_columns].ffill()
        elif autoFill != "None":
            raise Exception("AutoFill string format not correct.")

        # 5. Save final result as a NumPy array to match your existing interface
        self._final_array = df_sliced.values

    # --- Getters (Kept exactly identical to prevent breaking main.py) ---
    def get_final_list(self) -> np.ndarray:
        return self._final_array

    def get_starting_row(self) -> int:
        return self._starting_row

    def get_target_columns(self) -> list:
        return self._target_columns

    def get_asset_columns(self) -> list:
        return self._asset_columns
    
    def get_starting_date(self) -> str:
        return self._final_array[0][0]