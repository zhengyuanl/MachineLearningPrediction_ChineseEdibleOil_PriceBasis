import pandas as pd
import DateHandle
import matplotlib.pyplot as plt
from pathlib import Path

# 1. This always points to the folder containing THIS script, no matter what
SCRIPT_DIR = Path(__file__).resolve().parent

if __name__ == "__main__":
    vOilBasis = pd.read_csv(f"{SCRIPT_DIR}/vegetableOilBasis.csv", sep=',')
    vOilCash = pd.read_csv(f"{SCRIPT_DIR}/vegetableOilCash.csv", sep=",")
    vOilStock = pd.read_csv(f"{SCRIPT_DIR}/vegetableOilStock.csv", sep=',')

    vOilCombine = [["Date", "Cash", "Basis", "Stock"]]
    basisIndex = cashIndex = stockIndex = 0

    DateClass = DateHandle.DateSummoner(
        start_date_str="2008-01-01"
    )

    while DateClass.getCurrentDateString() != "2026-06-13":
        # print("Called======================")
        currentDate = DateClass.getCurrentDateString()
        tempList = [currentDate]

        # Bundle data sources, target columns, and their current tracking indices
        configs = [
            {"df": vOilCash,  "col": "Cash",  "idx": cashIndex},
            {"df": vOilBasis, "col": "Basis", "idx": basisIndex},
            {"df": vOilStock, "col": "Stock", "idx": stockIndex}
        ]

        # Process each dataset using a single shared logic block
        for item in configs:
            df, col, idx = item["df"], item["col"], item["idx"]
            
            if df["Date"][idx] == currentDate:
                tempList.append(df[col][idx])
                item["idx"] += 1
            else:
                tempList.append("")

        # Unpack the updated index values back into your tracking variables
        cashIndex  = configs[0]["idx"]
        basisIndex = configs[1]["idx"]
        stockIndex = configs[2]["idx"]
        vOilCombine.append(tempList)
        # print(tempList, "\n", "==========================")
        # print(tempList)
        

        DateClass.nextDate()

    # for count, each in enumerate(vOilCombine):
    #     # if(count == 100):
    #     #     break
    #     # print(each)
    #     for i in each:
    #         print(i, end="\t")
    #     print()
    
    # =========================================================================
    # PLOTTING CODE (Append this to the end of your script) (AI)
    # =========================================================================
    # 1. Convert the vOilCombine list into a DataFrame
    headers = vOilCombine[0]
    plot_df = pd.DataFrame(vOilCombine[1:], columns=headers)

    # 2. Convert Date column to datetime objects
    plot_df['Date'] = pd.to_datetime(plot_df['Date'])

    # 3. Clean the data columns and force empty strings into NaN numbers
    for col in ['Cash', 'Basis', 'Stock']:
        plot_df[col] = plot_df[col].astype(str).str.strip()
        plot_df[col] = pd.to_numeric(plot_df[col], errors='coerce')

    # 4. Create the main plot figure
    fig, ax1 = plt.subplots(figsize=(12, 6))

    # --- LINE 1: CASH (Left Y-Axis - Line Plot) ---
    color1 = '#1f77b4'
    line1 = ax1.plot(plot_df['Date'], plot_df['Cash'], label='Cash', color=color1, linewidth=2)
    ax1.set_xlabel('Date', fontsize=12)
    ax1.set_ylabel('Cash Value', color=color1, fontsize=12)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.grid(True, linestyle='--', alpha=0.3)

    # --- LINE 2: BASIS (Right Y-Axis - Line Plot) ---
    ax2 = ax1.twinx()
    color2 = '#ff7f0e'
    line2 = ax2.plot(plot_df['Date'], plot_df['Basis'], label='Basis', color=color2, linewidth=2)
    ax2.set_ylabel('Basis Value', color=color2, fontsize=12)
    ax2.tick_params(axis='y', labelcolor=color2)

    # --- LINE 3: STOCK (Far Right Y-Axis - SCATTER PLOT) ---
    ax3 = ax1.twinx()
    color3 = '#2ca02c'
    
    # Drop rows where Stock is NaN so scatter only plots the actual data points
    stock_clean = plot_df[['Date', 'Stock']].dropna()
    
    # Using scatter here fixes the invisible line problem
    scatter3 = ax3.scatter(stock_clean['Date'], stock_clean['Stock'], 
                           label='Stock', color=color3, s=10, edgecolors='black', zorder=5, marker='s', linewidths=0.5)
    
    # Offset the third y-axis so it doesn't overlap
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('Stock Value (Ton)', color=color3, fontsize=12)
    ax3.tick_params(axis='y', labelcolor=color3)

    # 5. Combined Legend for all axes (handles both lines and scatter markers)
    lines = line1 + line2 + [scatter3]
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc='upper left')

    # 6. Graph formatting and rendering
    plt.title('Vegetable Oil Market Data (Independent Y-Scales)', fontsize=14, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(f"{SCRIPT_DIR}/../CombinedData1.png", dpi=300, bbox_inches="tight")

    plt.show(block=False)

    plt.pause(0.1)
    
    with open("FinalVOil.csv", "w") as file:
        for lines in vOilCombine:
            for count, elements in enumerate(lines):
                file.write(
                    str(elements) + 
                    ("," if count != len(lines) - 1 else "")
                )
            file.write("\n")
    
    input("Press [ENTER] in this terminal to close the plot and exit.")