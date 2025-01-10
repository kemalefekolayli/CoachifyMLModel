import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# Load the mentor payments and student data
mentor_payments = pd.read_csv("cleaned_data/mentor_payments_summary.csv")
student_data = pd.read_csv("cleaned_data/student_list_combined_summary.csv")

# Step 1: Extract the list of mentors from the mentor_payments DataFrame
mentors = mentor_payments["MENTORLAR"].tolist()

# Step 2: Calculate total payments for each mentor
mentor_total_payment = {
    mentor: mentor_payments.loc[mentor_payments["MENTORLAR"] == mentor].iloc[:, 1:].sum(axis=1).values[0]
    for mentor in mentors
}

# Step 3: Calculate drop-out rates for each mentor
mentor_dropout_counts = {
    mentor: student_data[(student_data["Mentorunun Adı"] == mentor) & (student_data["Bıraktığı Ay"].notnull())].shape[0]
    for mentor in mentors
}
mentor_total_students = {
    mentor: student_data[student_data["Mentorunun Adı"] == mentor].shape[0]
    for mentor in mentors
}
mentor_dropout_rates = {
    mentor: (mentor_dropout_counts[mentor] / mentor_total_students[mentor]) if mentor_total_students[mentor] > 0 else 0
    for mentor in mentors
}

# Step 4: Combine payment and drop-out rate data into a DataFrame
mentor_analysis = pd.DataFrame(
    [
        {
            "Mentor": mentor,
            "Total Payment": mentor_total_payment[mentor],
            "Dropout Rate": round(mentor_dropout_rates[mentor], 2)
        }
        for mentor in mentors
    ]
)



# Step 5: Analyze correlation with a statistical test
correlation, p_value = pearsonr(mentor_analysis["Total Payment"], mentor_analysis["Dropout Rate"])
print(f"Correlation: {correlation}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("The correlation is statistically significant (p < 0.05).")
else:
    print("The correlation is not statistically significant (p >= 0.05).")

# Step 6: Visualize the relationship
plt.figure(figsize=(10, 6))
plt.scatter(mentor_analysis["Total Payment"], mentor_analysis["Dropout Rate"])
plt.title("Total Payment vs Dropout Rate")
plt.xlabel("Total Payment")
plt.ylabel("Dropout Rate")
plt.grid()
plt.show()

# Export the analysis data to a CSV file
mentor_analysis.to_csv("mentor_payment_dropout_analysis.csv", index=False)
print("Analysis data exported to mentor_payment_dropout_analysis.csv")
