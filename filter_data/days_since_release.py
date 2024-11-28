import pandas as pd
import datetime
import json

def calculate_days_since_release(data):
    # Calculate days since release using release_year, release_month, and release_day
    data['days_since_release'] = data.apply(
        lambda row: (datetime.datetime.now() - datetime.datetime(row['release_year'], row['release_month'], row['release_day'])).days,
        axis=1
    )
    return data

def process_sneaker_data(input_file, output_file):
    # Load data from the input JSON file
    data = pd.read_json(input_file)

    # Calculate days since release
    updated_data = calculate_days_since_release(data)

    # Save the updated data to the output JSON file
    updated_data.to_json(output_file, orient='records', indent=4)

    return updated_data