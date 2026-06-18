import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import math

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from pathlib import Path

# Self Made class to process data for the prediction
import DataProcessor

# 1. This always points to the folder containing THIS script, no matter what
SCRIPT_DIR = Path(__file__).resolve().parent

# warnings.filterwarnings("ignore")

def main():
    dataFilePath = f"{SCRIPT_DIR}/../OilPricePlot/FinalVOil.csv"

    X_target_columns = ["Date", "Cash", "Stock"]
    X_asset_columns = ["Cash", "Stock"]

    X_Data = DataProcessor.DataProcessor(
        file_path = dataFilePath,
        target_columns = X_target_columns,
        asset_columns = X_asset_columns,
        autoFill = "Repeat"
    )
    
    #==========================================#

    Y_target_columns = ["Date", "Basis"]
    Y_asset_columns = ["Basis"]

    Y_Data = DataProcessor.DataProcessor(
        file_path = dataFilePath,
        target_columns = Y_target_columns,
        asset_columns = Y_asset_columns
    )

    X = X_Data.get_final_list()
    y = Y_Data.get_final_list()

    DataProcessor.outputForm(X, "FinalXValue", X_target_columns)
    DataProcessor.outputForm(y, "FinalYValue", Y_target_columns)

    
    


if __name__ == "__main__":
    main()