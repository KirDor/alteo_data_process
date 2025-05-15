import json, os
import pandas as pd
from datetime import datetime

import argparse

def process_data(path,data_date):
    path_to_json = path
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

    # Open and read the JSON file
    json_data = []
    df_prod = None
    for d in json_files:
        date_str = d.split('_')[1][:8]
        date_obj = datetime.strptime(date_str, "%Y%m%d").strftime("%y-%m-%d")
        if date_obj == data_date:
            with open((path_to_json+d), 'r') as file:
                dict_to_json =json.load(file)
                # Check if there is different time-zon:
                if dict_to_json.get('tz') != "UTC":
                    print("Different timne-zone", dict_to_json.get('tz'))
                    # There isn't any other time-zone, so let's move on
                date = datetime.strptime(dict_to_json.get('measurement_ts'), "%Y-%m-%dT%H:%M:%S")
                prod_value = dict_to_json.get('production_rate')
                # Check timestamps are from 2025 March
                if date.year == 2025 and date.month == 3:
                    #Check normal values
                    if prod_value < 0 or prod_value > 3:
                        print(f"Warning: Production rate at {dict_to_json.get('mid')} outside the normal range (0 to 3).")
                        # For non-correct value use the previous reading value
                        dict_to_json['production_rate'] = measure_value
                    # Check sunlight hours
                    if date.hour<6 or date.hour>17:
                        # If the value is not 0
                        if prod_value != 0.0 :
                            # Print a warning message
                            print(f"Warning: Changing value at {dict_to_json.get('mid')} from {prod_value} to 0.")
                            dict_to_json['production_rate']=0
                    else:
                        # Save the next normal value to pass to non-correct values
                        measure_value = dict_to_json.get('production_rate')
                    json_data.append(dict_to_json)
    df = pd.DataFrame(json_data)

    if json_data and len(json_data) > 0:
        #Create aggregation
        df_prod = pd.DataFrame([{'sid': json_data[0]['sid'],'measurement_ts': json_data[0]['measurement_ts'][:10], 'aggreg_production_rate': df['production_rate'].sum()}])
    else:
        print("Error: json_data is empty or given date is invalid.")
    return df_prod

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Process path and date. Example format:--path ./jsons/jsons/ --data_date 25-03-18 ")
    
    # Define the 'path' and 'date' argument
    parser.add_argument("--path", type=str, required=True, help="Path to the data file")
    parser.add_argument("--data_date", type=str, required=True, help="Date of the data")

    # Parse the arguments
    args = parser.parse_args()

    result = process_data(args.path,args.data_date)

    # Access the 'path' and 'data_date' arguments
    print(f"Path: {args.path}")
    print(f"Data Date: {args.data_date}")
    print(result)

if __name__ == "__main__":
    main()

