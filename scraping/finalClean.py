import pandas as pd

# Step 1: Read the CSV file into a pandas DataFrame
data = pd.read_csv('./filtered_file.csv')
print(data.head())

# Step 2: Filter the DataFrame
filtered_data = data[(data['retail_price_eur'] >= 50) 
                     & (data['retail_price_eur'] <= 220)
                     & (data['lowest_price_eur'] <= 270)
                     & (data['instant_ship_lowest_price_eur'] <= 350)]

# Step 3: Write the filtered DataFrame to a new CSV file
filtered_data.to_csv('filtered_file.csv', index=False)