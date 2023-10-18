import pandas as pd

# Load the CSV file
doctors_df = pd.read_csv('doctors.csv')

# Split the "Name" column to extract the doctor's name and specialty
doctors_df[['Name', 'Specialities']] = doctors_df['Name'].str.split(',',n = 1, expand=True)
doctors_df['Specialities'].fillna("not available", inplace=True)

# Extract area of focus from the "Specialty" column by removing location details
doctors_df['Areas of Focus'] = doctors_df['Specialty'].str.replace(r'Location[s]*:[\r\n\t]+', '', regex=True)
doctors_df['Areas of Focus'].replace('', 'not available', inplace=True)

# Further clean the "Areas of Focus" column by removing any residual location details
doctors_df['Areas of Focus'] = doctors_df['Areas of Focus'].str.replace(r'[\r\n\t]+', '', regex=True)
doctors_df['Areas of Focus'] = doctors_df['Areas of Focus'].str.replace(r'Boston|Salem', 'not available', regex=True)

# Drop the original "Specialty" and "Department" columns
doctors_df.drop(columns=['Specialty', 'Department'], inplace=True)

# Add a new column "Hospital name" before the "Name" column
doctors_df.insert(0, 'Hospital Name', 'Massachusetts General Hospital')

# Save the cleaned data (optional)
doctors_df.to_csv('cleaned_data2.csv', index=False)

