import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from pathlib import Path
import DateHandle

# 1. This always points to the folder containing THIS script, no matter what
SCRIPT_DIR = Path(__file__).resolve().parent

# =========================================================================
# CONFIGURATION BLOCK (Add or remove variables here smoothly!)
# =========================================================================
# Format: "ColumnNameInOutput": {"filename": "yourfile.csv", "source_col": "ColumnNameInSource"}
DATA_CONFIG = {
    "Cash":      {"filename": "vegetableOilCash.csv",  "source_col": "Cash"},
    "Basis":     {"filename": "vegetableOilBasis.csv", "source_col": "Basis"},
    "Stock":     {"filename": "vegetableOilStock.csv", "source_col": "Stock"},
    "SOilStock": {"filename": "SOilStock.csv",         "source_col": "SOilStock"}
}

# The target date to stop processing
END_DATE_STR = "2026-06-13"

def main():
    # --- Dynamic Initialization ---
    all_columns = list(DATA_CONFIG.keys())
    
    # Pre-load dataframes and dynamically establish zero-start trackers for indexes
    datasets = {}
    for col, cfg in DATA_CONFIG.items():
        datasets[col] = {
            "df": pd.read_csv(f"{SCRIPT_DIR}/{cfg['filename']}", sep=','),
            "source_col": cfg["source_col"],
            "idx": 0  # Dynamic tracking pointer
        }

    # Initialize combined list with headers
    vOilCombine = [["Date"] + all_columns]

    DateClass = DateHandle.DateSummoner(start_date_str="2008-01-01")

    # =========================================================================
    # PROCESSING LOOP
    # =========================================================================
    while DateClass.getCurrentDateString() != END_DATE_STR:
        currentDate = DateClass.getCurrentDateString()
        tempList = [currentDate]

        # Process every configured data column dynamically
        for col in all_columns:
            data_meta = datasets[col]
            df = data_meta["df"]
            idx = data_meta["idx"]
            src_col = data_meta["source_col"]
            
            # CRITICAL SAFETY CHECK: Sync dates and match pointers safely
            if idx < len(df) and str(df["Date"].iloc[idx]).strip() == currentDate:
                tempList.append(df[src_col].iloc[idx])
                datasets[col]["idx"] += 1  # Increment pointer tracking for this feature
            else:
                tempList.append("")

        vOilCombine.append(tempList)
        DateClass.nextDate()

    # =========================================================================
    # PLOTTING CODE (Dynamic Multi-Axis Generation)
    # =========================================================================
    headers = vOilCombine[0]
    plot_df = pd.DataFrame(vOilCombine[1:], columns=headers)
    plot_df['Date'] = pd.to_datetime(plot_df['Date'])

    # Standard clean numeric parsing for all columns
    for col in all_columns:
        plot_df[col] = pd.to_numeric(plot_df[col].astype(str).str.strip(), errors='coerce')

    fig, ax1 = plt.subplots(figsize=(14, 7))
    plot_handles = []  # Accumulate axes plots for a unified single legend block

    # Primary Line: Cash Value
    color_cash = '#1f77b4'
    line1 = ax1.plot(plot_df['Date'], plot_df['Cash'], label='Cash', color=color_cash, linewidth=2)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Cash Value', color=color_cash, fontsize=12)
    ax1.tick_params(axis='y', labelcolor=color_cash)
    ax1.grid(True, linestyle='--', alpha=0.3)
    plot_handles.extend(line1)

    # Twin Axis 1: Basis Value
    ax2 = ax1.twinx()
    color_basis = '#ff7f0e'
    line2 = ax2.plot(plot_df['Date'], plot_df['Basis'], label='Basis', color=color_basis, linewidth=2)
    ax2.set_ylabel('Basis Value', color=color_basis, fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color_basis)
    plot_handles.extend(line2)

    # Twin Axis 2: Vegetable Oil Stock (Scatter)
    ax3 = ax1.twinx()
    color_stock = '#2ca02c'
    stock_clean = plot_df[['Date', 'Stock']].dropna()
    scatter3 = ax3.scatter(stock_clean['Date'], stock_clean['Stock'], 
                           label='Stock', color=color_stock, s=12, edgecolors='black', marker='s', zorder=5)
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('Stock Value (Ton)', color=color_stock, fontsize=12)
    ax3.tick_params(axis='y', labelcolor=color_stock)
    plot_handles.append(scatter3)

    # --- NEW ADDITION --- 
    # Twin Axis 3: Soybean Oil Stock (SOilStock)
    ax4 = ax1.twinx()
    color_soil = '#9467bd'  # Distinct purple shade
    soil_clean = plot_df[['Date', 'SOilStock']].dropna()
    line4 = ax4.plot(soil_clean['Date'], soil_clean['SOilStock'], 
                     label='SOilStock', color=color_soil, linewidth=1.5, linestyle=':')
    # Push the 4th axis further out to the right so it doesn't overlap existing axes
    ax4.spines['right'].set_position(('outward', 130))
    ax4.set_ylabel('Soybean Oil Stock Value (10k Ton)', color=color_soil, fontsize=12)
    ax4.tick_params(axis='y', labelcolor=color_soil)
    plot_handles.extend(line4)

    # Universal Combined Legend Block
    labels = [h.get_label() for h in plot_handles]
    ax1.legend(plot_handles, labels, loc='upper left')

    plt.title('Vegetable & Soybean Oil Market Data (Elastic Architecture)', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f"{SCRIPT_DIR}/../CombinedData1.png", dpi=300, bbox_inches="tight")
    plt.show(block=False)
    plt.pause(0.1)
    
    # =========================================================================
    # EXPORT CODE
    # =========================================================================
    output_path = f"{SCRIPT_DIR}/FinalVOil.csv"
    with open(output_path, "w") as file:
        for row in vOilCombine:
            file.write(",".join(str(element) for element in row) + "\n")
            
    print(f"\nProcessing complete! Consolidated matrix saved directly to: {output_path}")
    input("Press [ENTER] in this terminal to close the plot and exit.")

if __name__ == "__main__":
    main()