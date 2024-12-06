import pandas as pd

def csv_to_json(input_file, output_file):
    # Load the CSV file into a pandas DataFrame
    data = pd.read_csv(input_file)
    
    # Save the DataFrame to a JSON file
    data.to_json(output_file, orient='records', indent=4)

# Example usage
input_file = 'sneakers.csv'  # Replace with your actual input CSV file path
output_file = 'sneakers.json'  # Replace with your actual output JSON file path

csv_to_json(input_file, output_file)