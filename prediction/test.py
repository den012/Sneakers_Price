import pandas as pd
import sweetviz as sv

# Step 1: Load the Data
file_path = './filtered_file.csv'  # Update this to your file's path
data = pd.read_csv(file_path)

# Step 2: Generate a Sweetviz report
report = sv.analyze(data)

# Step 3: Save the report to an HTML file
report.show_html('sweetviz_report.html')