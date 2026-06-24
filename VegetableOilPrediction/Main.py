import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import math

from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
from pathlib import Path

# Self Made class to process data for the prediction
import DataProcessor

# 1. This always points to the folder containing THIS script, no matter what
SCRIPT_DIR = Path(__file__).resolve().parent

# warnings.filterwarnings("ignore")

def main():
    dataFilePath = f"{SCRIPT_DIR}/../OilPricePlot/FinalVOil.csv"

    X_target_columns = ["Date", "Cash", "Stock", "SOilStock"]
    X_asset_columns = ["Cash", "Stock", "SOilStock"]

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

    df_X = pd.DataFrame(X, columns=X_target_columns)
    df_y = pd.DataFrame(y, columns=Y_target_columns)

    df_X['Date'] = pd.to_datetime(df_X['Date'])
    df_y['Date'] = pd.to_datetime(df_y['Date'])

    df_merged = pd.merge(df_X, df_y, on='Date', how='left')

    # 4. Elastic Data Type Conversion
    # Dynamically loop through your X and Y asset columns to convert them to numeric
    numeric_cols = X_asset_columns + Y_asset_columns # Results in ["Cash", "Stock", "Basis"]
    
    for col in numeric_cols:
        if col in df_merged.columns:
            df_merged[col] = pd.to_numeric(df_merged[col], errors='coerce')

    # for lag in [1, 2, 4, 7]:
    #     df_merged[f'Cash_Lag_{lag}'] = df_merged['Cash'].shift(lag)
    #     df_merged[f'Stock_Lag_{lag}'] = df_merged['Stock'].shift(lag)    

    # # 2. Create Rolling Features (7-day and 30-day trends)
    # # We shift(1) first to prevent data leakage from the current day
    # df_merged['Cash_Roll_Mean_7'] = df_merged['Cash'].shift(1).rolling(window=7).mean()
    # df_merged['Stock_Roll_Mean_30'] = df_merged['Stock'].shift(1).rolling(window=30).mean()
    # df_merged['Cash_Roll_Std_7'] = df_merged['Cash'].shift(1).rolling(window=7).std()
    # df_merged['Cash_Momentum_7'] = df_merged['Cash'].shift(1) - df_merged['Cash'].shift(8)

    # Consider the season
    df_merged['Month'] = df_merged['Date'].dt.month
    
    df_merged['Target_Basis_7d'] = df_merged['Basis'].shift(-7)
    df_cleaned = df_merged.dropna().copy()

    feature_cols = [col for col in df_cleaned.columns if col not in ['Date', 'Basis', 'Target_Basis_7d']]
    print(feature_cols)

    X_final = df_cleaned[feature_cols]
    y_final = df_cleaned['Target_Basis_7d']

    print(df_cleaned.columns)
    print(f"Total matched pairs available for training: {len(df_cleaned)}")
    print(df_cleaned)

    split_idx = int(len(df_cleaned) * 0.8)

    X_train = X_final.iloc[:split_idx]
    X_test = X_final.iloc[split_idx:]
    y_train = y_final.iloc[:split_idx]
    y_test = y_final.iloc[split_idx:]

    regressor = XGBRegressor(
        n_estimators=150,     # Number of sequential gradient trees
        learning_rate=0.05,   # Step size shrinkage to prevent overfitting
        max_depth=5,          # Shallow trees deal better with noisy market data
        subsample=0.8,        # Sample 80% of data to prevent overfitting
        colsample_bytree=0.8, # Sample 80% of features per tree
        random_state=42
    )

    regressor.fit(X_train, y_train)

    y_pred = regressor.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)
    print("Mean Squared Error:", mse)

    r2 = r2_score(y_test, y_pred)
    print("R-squared:", r2)

    # --- Fix Plotting for Multi-variable ---
    plt.figure(figsize=(8, 6))
    
    # Scatter plot of actual vs predicted on the TEST set
    plt.scatter(y_test, y_pred, color='blue', alpha=0.6, label="Predicted vs Actual")
    
    # A perfect 45-degree line for reference
    perfect_line = np.linspace(min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max()), 100)
    plt.plot(perfect_line, perfect_line, color='red', linestyle='--', label="Perfect Prediction")

    plt.title("Random Forest: Actual vs Predicted Target_Basis_14d")
    plt.xlabel('Actual Target_Basis_14d')
    plt.ylabel('Predicted Target_Basis_14d')
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{SCRIPT_DIR}/Predict1.png", dpi=300, bbox_inches="tight")

    plt.show()

    # --- Time-Series Trend Line Plot ---
    
    # 1. Grab the corresponding dates for the test set
    test_dates = df_cleaned['Date'].iloc[split_idx:]

    # 2. Create a temporary DataFrame to hold dates, actuals, and predictions
    # This ensures everything stays perfectly aligned and sorted chronologically
    df_plot = pd.DataFrame({
        'Date': test_dates,
        'Actual': y_test,
        'Predicted': y_pred
    }).sort_values('Date') # Sort by date just in case

    # 3. Plot the trends
    plt.figure(figsize=(14, 7))
    
    plt.plot(df_plot['Date'], df_plot['Actual'], color='blue', label='Actual Basis', linewidth=2)
    plt.plot(df_plot['Date'], df_plot['Predicted'], color='orange', label='Predicted Basis', linewidth=2, linestyle='--')

    # Formatting the plot
    plt.title("Vegetable Oil Basis: Actual vs. Predicted Trends (Test Set)", fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Basis Spread', fontsize=12)
    plt.legend(fontsize=11, loc='upper left')
    plt.grid(True, linestyle=':', alpha=0.6)
    
    # Rotate date labels automatically so they don't overlap
    plt.gcf().autofmt_xdate() 
    plt.savefig(f"{SCRIPT_DIR}/Predict.png", dpi=300, bbox_inches="tight")
    plt.show()

    # DataProcessor.outputForm(X, "FinalXValue", X_target_columns)
    # DataProcessor.outputForm(y, "FinalYValue", Y_target_columns)

if __name__ == "__main__":
    main()