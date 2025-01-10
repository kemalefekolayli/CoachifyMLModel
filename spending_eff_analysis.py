import pandas as pd
import matplotlib.pyplot as plt

# Load the mentor payments and student data
mentor_payments = pd.read_csv("cleaned_data/mentor_payments_summary.csv")
student_data = pd.read_csv("cleaned_data/student_list_combined_summary.csv")

# Step 1: Extract the list of mentors from the mentor_payments DataFrame
mentors = mentor_payments["MENTORLAR"].tolist()

# Step 2: Initialize a dictionary to track student counts, total retention time, and payments for each mentor
mentor_student_counts = {mentor: 0 for mentor in mentors}
mentor_total_retention = {mentor: 0 for mentor in mentors}
mentor_total_payment = {mentor: 0 for mentor in mentors}

# Step 3: Count students and calculate total retention time for each mentor
for mentor in mentors:
    # Special case: Search "Feyza Karayel" as "Ferhunde Feyza Karayel"
    search_name = "Feyza Karayel" if mentor == "Ferhunde Feyza Karayel" else mentor

    # Filter the student list for the current mentor
    mentor_students = student_data[student_data["Mentorunun Adı"] == search_name]
    
    # Update the student count
    student_count = mentor_students.shape[0]
    mentor_student_counts[mentor] = student_count

    # Calculate total retention time by summing the "Months Active" column
    total_retention = mentor_students["Months Active"].sum()
    mentor_total_retention[mentor] = total_retention

# Step 4: Calculate total payments for each mentor
for _, row in mentor_payments.iterrows():
    mentor = row["MENTORLAR"]
    if mentor in mentor_total_payment:
        mentor_total_payment[mentor] = row.iloc[1:].sum()  # Sum payments across all months

# Step 5: Calculate the average retention time for each mentor
mentor_average_retention = {
    mentor: float(round((mentor_total_retention[mentor] / mentor_student_counts[mentor]), 2)) if mentor_student_counts[mentor] > 0 else 0.0
    for mentor in mentors
}

# Step 6: Calculate cost per student (Cost Efficiency)
mentor_cost_efficiency = {
    mentor: float(round((mentor_total_payment[mentor] / mentor_student_counts[mentor]), 2)) if mentor_student_counts[mentor] > 0 else float('inf')
    for mentor in mentors
}

# Step 7: Combine the results into a DataFrame
mentor_summary = pd.DataFrame(
    [
        {
            "Mentor": mentor,
            "Student Count": mentor_student_counts[mentor],
            "Average Retention": mentor_average_retention[mentor],
            "Total Payment": round(mentor_total_payment[mentor], 2),
            "Cost Efficiency": mentor_cost_efficiency[mentor]
        }
        for mentor in mentors
    ]
)

# Step 8: Add rankings for individual metrics
mentor_summary["Student Count Rank"] = mentor_summary["Student Count"].rank(ascending=False, method="min")
mentor_summary["Retention Rank"] = mentor_summary["Average Retention"].rank(ascending=False, method="min")
mentor_summary["Cost Efficiency Rank"] = mentor_summary["Cost Efficiency"].rank(ascending=True, method="min")

# Step 9: Calculate a composite score and rank mentors
mentor_summary["Composite Score"] = (
    0.4 * mentor_summary["Average Retention"] +
    0.4 * (1 / mentor_summary["Cost Efficiency"]).replace([float('inf')], 0) +  # Invert cost efficiency (lower is better)
    0.2 * mentor_summary["Student Count"]
)
mentor_summary["Composite Rank"] = mentor_summary["Composite Score"].rank(ascending=False, method="min")

# Step 10: Export the summary to a CSV file
output_path = "mentor_summary.csv"
mentor_summary.to_csv(output_path, index=False)

print(f"Mentor summary has been exported to {output_path}")
