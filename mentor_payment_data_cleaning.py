import pandas as pd
import os

# Ensure the cleaned_data directory exists
os.makedirs("cleaned_data", exist_ok=True)

# Load mentor payments data
mentor_path = "data/Mentor Ödemeleri.xlsx"

# Load all sheet names
mentor_sheets = pd.ExcelFile(mentor_path).sheet_names

# Define mentors to ignore
ignore_mentors = ["Kemal Efe Kolaylı", "Efe Çalış"]

# Initialize an empty dictionary to hold monthly payments for each mentor
mentor_payment_dict = {}

# Process each sheet (representing a month)
for sheet_name in mentor_sheets:
    # Skip the last sheet (assume "Kemal - Efe" is the last one)
    if sheet_name == "Kemal - Efe":
        continue

    print(f"\nProcessing sheet: {sheet_name}")
    # Read the sheet
    mentor_data = pd.read_excel(mentor_path, sheet_name=sheet_name)

    # Drop fully empty rows and columns
    mentor_data_cleaned = mentor_data.dropna(how="all", axis=0).dropna(how="all", axis=1)

    # Skip rows for ignored mentors
    mentor_data_cleaned = mentor_data_cleaned[~mentor_data_cleaned.iloc[:, 0].isin(ignore_mentors)]

    # Ensure the first column is "Mentor"
    mentor_data_cleaned.columns = ["Mentor"] + [f"Payment{i}" for i in range(1, len(mentor_data_cleaned.columns))]

    # Convert payment columns to numeric
    for col in mentor_data_cleaned.columns[1:]:
        mentor_data_cleaned[col] = pd.to_numeric(mentor_data_cleaned[col], errors="coerce")

    # Aggregate payments for each mentor in the current sheet
    for _, row in mentor_data_cleaned.iterrows():
        mentor = row["Mentor"]
        total_payment = row[1:].sum(skipna=True)  # Sum all payment columns, ignoring NaN

        # Initialize mentor in the dictionary if not present
        if mentor not in mentor_payment_dict:
            mentor_payment_dict[mentor] = {}

        # Add the total payment for the current month
        mentor_payment_dict[mentor][sheet_name] = mentor_payment_dict[mentor].get(sheet_name, 0) + total_payment

# Convert the dictionary to a DataFrame
mentor_payment_df = pd.DataFrame.from_dict(mentor_payment_dict, orient="index").fillna(0)

# Add a "Total" column to show the total money spent for each mentor
mentor_payment_df["Total"] = mentor_payment_df.sum(axis=1)

# Save the final cleaned data to CSV
mentor_payment_df.to_csv("cleaned_data/mentor_payments_summary.csv")

print("\nMentor payment aggregation completed.")
print("Final summary saved to 'cleaned_data/mentor_payments_summary.csv'")
