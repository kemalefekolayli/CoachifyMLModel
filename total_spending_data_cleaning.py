import pandas as pd
import os

# Ensure the cleaned_data directory exists
os.makedirs("cleaned_data", exist_ok=True)

# Load the messy data file
file_path = "data/REKLAM VE DİĞER.xlsx"

# Turkish to English month mapping
month_mapping = {
    "Ocak": "January",
    "Şubat": "February",
    "Mart": "March",
    "Nisan": "April",
    "Mayıs": "May",
    "Haziran": "June",
    "Temmuz": "July",
    "Ağustos": "August",
    "Eylül": "September",
    "Ekim": "October",
    "Kasım": "November",
    "Aralık": "December",
}

# Step 1: Load data and skip rows 2-41 but keep the header (first row)
data = pd.read_excel(file_path, skiprows=list(range(1, 41)), header=0)  # Skip rows 2-41, retain the header

# Step 2: Drop rows where 'HARCAMAYI YAPAN KİŞİ' is empty
if "HARCAMAYI YAPAN KİŞİ" in data.columns:
    data = data.dropna(subset=["HARCAMAYI YAPAN KİŞİ"])
else:
    print("Warning: 'HARCAMAYI YAPAN KİŞİ' column not found.")

# Step 3: Simplify 'TARİH' to only the month name
def simplify_month(row):
    if pd.notnull(row["TARİH"]):
        for turkish_month, english_month in month_mapping.items():
            if turkish_month in str(row["TARİH"]):
                return english_month  # Return only the month name
    return "Unknown"

if "TARİH" in data.columns:
    data["PAYMENT MONTH"] = data.apply(simplify_month, axis=1)
else:
    print("No 'TARİH' column found. 'PAYMENT MONTH' will be set to 'Unknown'.")
    data["PAYMENT MONTH"] = "Unknown"

# Step 4: Remove unnecessary columns
columns_to_remove = ["ÖDEME DURUMU", "AÇIKLAMA", "ÖDEME YÖNTEMİ", "TARİH"]
data = data.drop(columns=[col for col in columns_to_remove if col in data.columns], errors="ignore")

# Step 5: Finalize the cleaned dataset
data["PAYMENT MONTH"] = data["PAYMENT MONTH"].fillna("Unknown")

# Save the final cleaned dataset
final_output_path = "cleaned_data/reklam_and_other_cleaned.csv"
data.to_csv(final_output_path, index=False)

print("\nFinal cleaned data saved to:")
print(final_output_path)
