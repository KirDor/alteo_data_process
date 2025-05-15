# alteo_data_process
Measurements data files processing

This script is designed to process JSON files from a specified directory, extract data based on a specific date, and perform some validation and aggregation on the data.
To run the given Python script from the command line, you'll need to provide the required arguments using the `argparse` module's command-line interface. 

### Prerequisites:
- Ensure Python is installed on your system.
- Save the script in a `.py` format.
- Intstall Used libaries (see below)

### Required Arguments:
1. **`--path`**: This argument specifies the directory path where the JSON files are located.
2. **`--data_date`**: This argument specifies the date for filtering the data. The date should be in the format "yy-mm-dd".

### Command-Line Execution:

**Run the Script with Arguments**:
   - Execute the script using the `python` command followed by the script name and provide the required arguments `--path` and `--data_date`. For example:
     ```bash
     python process_data.py --path /path/to/json/files --data_date 25-03-18
     ```

   - Replace `/path/to/json/files` with the actual path to the directory containing your JSON files.
   - Replace `25-03-18` with the actual date you want to use for filtering the data.

### Notes:
- Ensure that the path and date are correctly formatted and valid.
- The script assumes that the JSON files have a specific naming convention and contain expected data fields, so ensure your files match these expectations.


### Used libaries:
1. json: Used to parse JSON files.
2. os: Provides functions for interacting with the operating system, particularly to list files in a directory.
3. pandas Used for data manipulation and analysis, specifically to create and handle dataframes.
4. datetime Used to work with date and time objects.
5. argparse: Used to handle command-line arguments.

### Function Definitions:

#### `process_data(path, data_date)`:
- **Purpose**: To read JSON files from a directory, filter data based on a provided date, validate the data, and aggregate production rates.
- **Parameters**:
  - `path`: Directory path containing JSON files.
  - `data_date`: Date string in "yy-mm-dd" format to filter data.

- **Functionality**:
  1. **List JSON Files**: 
     - Uses `os.listdir()` to list all files in the directory specified by `path`.
     - Filters files that end with `.json`.

  2. **Read and Filter JSON Data**:
     - Initializes an empty list `json_data` and a variable `df_prod` as `None`.
     - Iterates over each JSON file:
       - Extracts the date from the filename and converts it to a date object.
       - Checks if the extracted date matches `data_date`.
       - Reads the JSON file content into a dictionary (`dict_to_json`).

  3. **Timezone Check**:
     - Checks if the 'tz' (timezone) in the JSON data is "UTC".
     - Prints a message if the timezone is different (although the script doesn't handle different timezones beyond printing a message).

  4. **Data Validation**:
     - Converts the `measurement_ts` (timestamp) to a `datetime` object.
     - Checks if the data's year is 2025 and month is March.
     - Validates the `production_rate` to ensure it is between 0 and 3; if not, it uses the previous valid value (`measure_value`).
     - Checks if the timestamp hour is between 6 and 17 (sunlight hours); if not, it sets `production_rate` to 0 and prints a warning.

  5. **Data Aggregation**:
     - If `json_data` is not empty, aggregates the `production_rate` values into a dataframe `df_prod`.
     - Returns `df_prod` or prints an error if `json_data` is empty or invalid.

### Main Function:

#### `main()`:
- **Purpose**: To parse command-line arguments, call the `process_data` function, and print results.
- **Functionality**:
  1. **Argument Parsing**:
     - Uses `argparse` to define and parse `--path` and `--data_date` arguments.
     - `--path`: Path to the directory containing JSON files.
     - `--data_date`: Date to filter data in the format "yy-mm-dd".

  2. **Function Call**:
     - Calls `process_data()` with parsed arguments.
     - Prints the path, data date, and result from `process_data()`.

### Execution:
- The script executes the `main()` function only if the script is run directly (not imported as a module).

### Usage:
- Run the script from the command line with the format:
  ```
  python script_name.py --path <directory_path> --data_date <date_in_yy-mm-dd_format>
  ```

## Notes

- I did not upload any data files, in accordance with the instructions.
- I used an LLM (ChatGPT) for help with JSON validation and refining the usage of argparse.
