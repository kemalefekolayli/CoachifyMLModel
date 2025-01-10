import pandas as pd
import os
from datetime import datetime

# Ensure the cleaned_data directory exists
os.makedirs("cleaned_data", exist_ok=True)

# Load the student file
student_file_path = "data/Öğrenci Listesi.xlsx"

# Define the sheets to process
sheet_names = ["24-25 SEZONU", "23-24 SEZONU"]

# Initialize an empty DataFrame to hold the combined data
all_student_data_cleaned = pd.DataFrame()

# Define a mapping of month names to numeric values
month_mapping = {
    "Ocak": 1,
    "Şubat": 2,
    "Mart": 3,
    "Nisan": 4,
    "Mayıs": 5,
    "Haziran": 6,
    "Temmuz": 7,
    "Ağustos": 8,
    "Eylül": 9,
    "Ekim": 10,
    "Kasım": 11,
    "Aralık": 12,
}

# Define the current date as Ocak 2025
current_date = datetime(2025, 1, 1)

# Process each sheet
for sheet_name in sheet_names:
    print(f"\nProcessing sheet: {sheet_name}")
    # Load the sheet
    student_data = pd.read_excel(student_file_path, sheet_name=sheet_name)

    # Select relevant columns
    columns_of_interest = ["Öğrenci Adı", "Mentorunun Adı", "ÜB Ay", "Bıraktığı Ay"]
    student_data_cleaned = student_data[columns_of_interest]

    # Drop rows with missing student names or start months
    student_data_cleaned = student_data_cleaned.dropna(subset=["Öğrenci Adı", "ÜB Ay"])

    # Assign the start year based on the season and month
    season_start_year, season_end_year = map(int, sheet_name.split(" ")[0].split("-"))

    def assign_start_year(ub_ay):
        month = ub_ay.split()[0]
        if sheet_name == "23-24 SEZONU" and month in ["Ocak", "Şubat", "Mart", "Nisan"]:
            return season_end_year  # Start year is 2024 for these months
        return season_start_year

    student_data_cleaned["Start Year"] = student_data_cleaned["ÜB Ay"].apply(assign_start_year)
    student_data_cleaned["Season"] = sheet_name

    # Convert months to datetime objects using the assigned start year
    def convert_to_datetime(value, start_year):
        month = value.split()[0]
        return datetime(start_year, month_mapping.get(month, 6), 1)

    student_data_cleaned["ÜB Ay"] = student_data_cleaned.apply(
        lambda row: convert_to_datetime(row["ÜB Ay"], row["Start Year"]), axis=1
    )

    # Append the cleaned data to the combined DataFrame
    all_student_data_cleaned = pd.concat([all_student_data_cleaned, student_data_cleaned], ignore_index=True)

# Adjust months active and handle users with missing end dates
def adjust_months_active(row):
    # Handle end date
    if pd.isnull(row["Bıraktığı Ay"]) or row["Bıraktığı Ay"] == "":
        end_date = current_date
    else:
        end_date = convert_to_datetime(row["Bıraktığı Ay"], row["ÜB Ay"].year)

    # Calculate months active
    months_active = (end_date.year - row["ÜB Ay"].year) * 12 + (end_date.month - row["ÜB Ay"].month)

    # Fix negative months active
    if months_active < 0:
        end_date = datetime(2024, end_date.month, 1)
        months_active = (end_date.year - row["ÜB Ay"].year) * 12 + (end_date.month - row["ÜB Ay"].month)

    row["Bıraktığı Ay"] = end_date
    row["Months Active"] = months_active
    return row

all_student_data_cleaned = all_student_data_cleaned.apply(adjust_months_active, axis=1)

# Filter to correct months active values over 1000
all_student_data_cleaned.loc[all_student_data_cleaned["Months Active"] > 1000, "Months Active"] -= 24000

# Debug: Print a preview of the combined cleaned data
print("\nCombined Cleaned Student Data Preview:")
print(all_student_data_cleaned.head())

# Save the combined cleaned data to CSV with proper encoding
output_path = "cleaned_data/student_list_combined_summary.csv"
all_student_data_cleaned.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\nStudent data cleaning completed for both seasons.")
print(f"Combined cleaned data saved to '{output_path}'")
