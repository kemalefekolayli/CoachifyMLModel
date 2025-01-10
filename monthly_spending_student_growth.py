import pandas as pd

# File paths
student_data_file = "cleaned_data/student_list_combined_summary.csv"
spending_data_file = "cleaned_data/Spending_data.txt"

# Load the student data
student_data = pd.read_csv(student_data_file)

# Initialize data structures
monthly_student_gain = {str(month).zfill(2): 0 for month in range(1, 13)}
monthly_spending = {str(month).zfill(2): [] for month in range(1, 13)}  # Store category spending breakdown
monthly_total_spending = {str(month).zfill(2): 0 for month in range(1, 13)}

# Helper function to map Turkish month names to numeric values
month_mapping = {
    "Ocak": "01", "Şubat": "02", "Mart": "03", "Nisan": "04", "Mayıs": "05",
    "Haziran": "06", "Temmuz": "07", "Ağustos": "08", "Eylül": "09", "Ekim": "10",
    "Kasım": "11", "Aralık": "12"
}

# Helper function to check if a string can be converted to a float
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Step 1: Calculate student gain for each month
for _, row in student_data.iterrows():
    ub_ay = str(row["ÜB Ay"])

    # Skip if the year is not 0024
    if not ub_ay.startswith("0024"):
        continue

    # Extract the month from the date
    month = ub_ay[5:7]

    # Update the count for the month
    if month in monthly_student_gain:
        monthly_student_gain[month] += 1

# Step 2: Parse spending data from text file
current_month = None
with open(spending_data_file, "r", encoding="utf-8") as file:
    for line in file:
        line = line.strip()

        # Check if the line matches a month name
        if line in month_mapping:
            current_month = month_mapping[line]
            continue

        # Skip lines without a current month
        if not current_month:
            continue

        # Parse spending category and amount
        if line.lower().startswith("toplam"):
            total = line.split()[-1].replace(".", "").replace(",", ".")
            if is_float(total):
                monthly_total_spending[current_month] = float(total)
            else:
                print(f"Invalid total value for {current_month}: {total}, skipping...")
            current_month = None  # Reset after processing `Toplam`
        else:
            parts = line.split()
            if len(parts) > 1:
                category = " ".join(parts[:-1])  # Use all but the last word as the category
                amount = parts[-1].replace(".", "").replace(",", ".")
                if is_float(amount):
                    monthly_spending[current_month].append({
                        "Category": category,
                        "Amount": float(amount)
                    })
                else:
                    print(f"Invalid amount for category '{category}' in {current_month}: {amount}")

# Step 3: Calculate Total ROI for Each Month
roi_data = []
for month, spending_list in monthly_spending.items():
    student_gain = monthly_student_gain[month]
    total_spending = monthly_total_spending[month]

    # Determine value per student based on the month
    if month in ["01", "02", "03", "04", "05", "06"]:  # Ocak - Haziran
        value_per_student = 650
    elif month == "07":  # Temmuz
        value_per_student = 750
    else:  # Ağustos - Aralık
        value_per_student = 850

    total_value = student_gain * value_per_student
    total_roi = total_value / total_spending if total_spending > 0 else 0

    # Format spending breakdown for CSV
    spending_breakdown = {entry["Category"]: entry["Amount"] for entry in spending_list}

    roi_data.append({
        "Month": month,
        "Student Gain": student_gain,
        "Total Spending": total_spending,
        "Total ROI": total_roi,
        **spending_breakdown  # Expand spending breakdown into columns
    })

# Convert ROI data to DataFrame
roi_df = pd.DataFrame(roi_data)

# Save the results to a CSV file
roi_df.to_csv("cleaned_data/monthly_roi_summary.csv", index=False)

# Print the results
print("Monthly ROI Summary saved to cleaned_data/monthly_roi_summary.csv")
