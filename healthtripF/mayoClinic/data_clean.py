import pandas as pd

# Load the data
data = pd.read_csv("scraped_data.csv")

# Remove Rows with Missing Values
cleaned_data = data.dropna(how='all')

# Trim Whitespace using an explicit loop
cleaned_data = cleaned_data.map(lambda x: x.strip() if isinstance(x, str) else x)


# Remove Duplicate Rows
cleaned_data = cleaned_data.drop_duplicates()

# Add "Hospital Name" column before the "Name" column and fill with "Mayo Clinic"
cleaned_data.insert(0, 'Hospital Name', 'Mayo Clinic')

# Remove the "Locations" column
cleaned_data = cleaned_data.drop(columns=['Locations'])


# Save the cleaned data to a new CSV file
cleaned_data_path = "cleaned_scraped_data.csv"
cleaned_data.to_csv(cleaned_data_path, index=False)
