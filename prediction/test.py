# import pandas as pd
# import sweetviz as sv

# # Step 1: Load the Data
# file_path = './filtered_file.csv'  # Update this to your file's path
# data = pd.read_csv(file_path)

# # Step 2: Generate a Sweetviz report
# report = sv.analyze(data)

# # Step 3: Save the report to an HTML file
# report.show_html('sweetviz_report.html')

import pandas as pd

# Load the CSV file with semicolons as delimiters
df = pd.read_csv("./test_model.csv", delimiter=';')

# Save the CSV file with commas as delimiters
df.to_csv("./test_model.csv", index=False)