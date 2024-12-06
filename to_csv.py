import pandas as pd
import json

input_file = 'sneakers.json'
output_file = 'sneakers.csv'  

# Load the JSON data
with open(input_file, 'r') as file:
    data = json.load(file)

# Convert the JSON data to a DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)