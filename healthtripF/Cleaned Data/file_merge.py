import os
import pandas as pd

# Set the directory where your CSV files are located
csv_directory = 'Cleaned Data/All files'

# Get a list of all CSV files in the directory
csv_files = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through the CSV files and append their data to the merged_data DataFrame
for file in csv_files:
    file_path = os.path.join(csv_directory, file)
    data = pd.read_csv(file_path)
    merged_data = merged_data._append(data, ignore_index=True)

# Save the merged data to a new CSV file
merged_data.to_csv('C:/Users/FuZ/Desktop/healthtrip/Cleaned Data/all_cleaned_merged.csv', index=False)

print("Merged CSV files successfully.")
