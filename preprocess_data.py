import pandas as pd
import numpy as np
import json
import os

def preprocess_json():
    # Read the JSON file

    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("HEY!")
    # Construct the path to the data file
    data_file_path = os.path.join(script_dir, '..', 'data', 'gp_data.json')

    with open(data_file_path, "r") as file:
        data = json.load(file)

    # Flatten the data so each list entry becomes a separate row
    flat_data = []
    for entry in data:
        # Get the length of the lists (assume all lists are of the same length)
        list_length = len(entry['avg_high_price'])
        for i in range(list_length):
            flat_entry = {key: entry[key][i] if isinstance(entry[key], list) else entry[key] for key in entry}
            flat_data.append(flat_entry)

    # Convert the flattened data to a DataFrame
    df = pd.DataFrame(flat_data)

    # Replace 'None' values with np.nan
    df.replace('None', np.nan, inplace=True)

    # Handle missing values and convert data types if necessary
    df.ffill(inplace=True)
    df.bfill(inplace=True)

    # Save the preprocessed data to a CSV file
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the data file
    data_file_path = os.path.join(script_dir, '..', 'data', 'preprocessed_data.csv')
    df.to_csv(data_file_path, index=False)

def preprocess_csv():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the data file
    data_file_path = os.path.join(script_dir, '..', 'data', 'preprocessed_data.csv')
    df = pd.read_csv(data_file_path)

    # Create time-based features
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek

    # Lag features are the previous prices for a row
    lag_features = ['avg_high_price', 'avg_low_price', 'low_price_volume']
    for feature in lag_features:
        for lag in range(1, 5):  # Creating lag features for the past 4 time steps
            df[f'{feature}_lag_{lag}'] = df[feature].shift(lag)

    # Drop rows with NaN values created by lag features
    df.dropna(inplace=True)

    # Drop the original timestamp column
    df.drop(columns=['timestamp'], inplace=True)

    # Save
    df.to_csv(data_file_path, index=False)

if __name__ == '__main__':
    preprocess_json()
    preprocess_csv()

