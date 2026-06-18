# DataProcessor Class Documentation

Library written by Charlie Liu

The `DataProcessor` class is designed to automate the initial validation, extraction, and forward-filling of financial asset pricing data. It ingestion-validates configuration limits, locates the first historical row containing valid data across multiple target asset criteria, and fills any missing (`NaN`) downstream observations using a historical forward-carry sequence. All primary computation is done instantly upon instantiation to ensure optimal data availability.

Class Signature
---------------

Python

    class DataProcessor:
        def __init__(self, file_path: str, target_columns: list, asset_columns: list, autoFill)

Architectural Workflow
----------------------

The class follows a linear execution architecture handled completely within the object initialization cycle:

1.  **Validation**: Confirms file existence and verifies that all requested configuration columns reside within the source dataset.
    
2.  **First-Valid Discovery**: Scans target asset columns to find the earliest indexing row containing non-null data across all designated financial assets (`starting_row`).
    
3.  **Data Imputation (Forward-Fill)**: Processes chronological entries starting from the `starting_row`. If an entry encounters an invalid element (`NaN`), it overwrites it dynamically with the last historically verified real number for that specific asset tracking pool.
    
4.  **Data Slicing**: Clips the operational matrix to remove historical leading padding rows where asset prices were missing, formatting it for consumption.
    

Constructor Details
-------------------

### `__init__(file_path, target_columns, asset_columns)`

Initializes the pipeline and performs all mutation/processing calculations immediately.

#### Parameters

*   **`file_path`** (`str`): The relative or absolute file path to the source CSV file containing the raw pricing information.
    
*   **`target_columns`** (`list` of `str`): A structural array containing all column names to be pulled from the CSV (e.g., `["Date", "Cash", "Stock", "Basis"]`).
    
*   **`asset_columns`** (`list` of `str`): The subset of `target_columns` explicitly tracked for forward-fill operations (e.g., `["Cash", "Stock"]`). It also signify that value that is useful for the prediction.
    
*   **`autoFill`:** 

    - `"Repeat"` Fill the NaN block with previous value
    - `"None"` No autofill

#### Critical Exceptions Raised

*   **`Exception("Target Columns has to contain Asset Columns")`**: Raised if an asset metric is provided that does not exist in the broader targeted context parameters.
    
*   **`Exception("Parameter in Target Columns does not exist")`**: Raised if a specified column name cannot be verified inside the actual CSV header collection.
    

API Reference (Getters)
-----------------------

### `get_final_list()`

Returns the mutated matrix after execution completes. Leading dead-zones before valid tracking are automatically truncated.

*   **Returns:** `numpy.ndarray` — A 2D NumPy array starting explicitly from the verified baseline timestamp row.
    

### `get_starting_row()`

Exposes the exact structural index mapping where valid tracking metrics begin inside the raw dataset.

*   **Returns:** `int` — The baseline index mapping offset.
    

### `get_target_columns()`

Exposes the structural listing of properties used during parsing limits.

*   **Returns:** `list` of `str` — Original target column elements array.
    

### `get_asset_columns()`

Exposes tracking sub-elements being systematically watched for forward-fill mutations.

*   **Returns:** `list` of `str` — Original tracking assets configuration array.
    

Integration Example
-------------------

Python

    import os
    from your_module import DataProcessor
    
    def main():
        # Setup configuration environment paths
        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
        csv_path = f"{SCRIPT_DIR}/../OilPricePlot/FinalVOil.csv"
        
        target_cols = ["Date", "Cash", "Stock", "Basis"]
        asset_cols = ["Cash", "Stock"]
    
        # 1. Instantiate the Processor (Processes data immediately)
        processor = DataProcessor(
            file_path=csv_path, 
            target_columns=target_cols, 
            asset_columns=asset_cols
        )
    
        # 2. Extract calculations via public access APIs
        starting_index = processor.get_starting_row()
        cleaned_dataset = processor.get_final_list() # Returns raw NumPy array
    
        print(f"Data validated. Active tracking began at base index: {starting_index}")
        print(f"Operational Array Shape: {cleaned_dataset.shape}")
    
    if __name__ == "__main__":
        main()
