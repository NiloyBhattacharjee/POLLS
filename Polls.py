import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
# Define the colors for the bars
dem_color = "#0072B2"  # blue
rep_color = "#D55E00"  # orange
# Load the data into a Pandas dataframe
df = pd.read_csv("/home/niloybhattacharjee/POLLS/bod_fortune_500_DIME.csv")

# Remove duplicates
df = df.drop_duplicates()

# Convert missing values to NaN
df = df.replace(["NA", "nan", "N/A"], pd.NA)

# Check for outliers and remove them if necessary

# Check the data types of each column
df.dtypes

# Check data types
print(df.dtypes)

# Convert data types if necessary
df["age"] = pd.to_numeric(df["age"], errors="coerce")
df["dime.cfscore"] = pd.to_numeric(df["dime.cfscore"], errors="coerce")


# Rename column headers
df = df.rename(columns={
    "dime.cid": "company_id",
    "corp.person.id": "person_id",
    "ticker": "company_ticker",
    "corp.name": "company_name",
    "last.name": "last_name",
    "first.name": "first_name",
    "middle.name": "middle_name",
    "age": "person_age",
    "gender": "person_gender",
    "ceo": "is_ceo",
    "chairman": "is_chairman",
    "privatefirm": "is_private_firm",
    "sector": "company_sector",
    "industry": "company_industry",
    "dime.cfscore": "company_cfscore",
    "total": "total_donations",
    "num.conts": "num_contributions",
    "self.funded": "self_funded",
    "total.dem": "total_dem_donations",
    "total.rep": "total_rep_donations",
    "pct.to.dems": "percent_to_dem_donations",
    "total.2002": "total_donations_2002",
    "total.2004": "total_donations_2004",
    "total.2006": "total_donations_2006",
    "total.2008": "total_donations_2008",
    "total.2010": "total_donations_2010",
    "total.2012": "total_donations_2012",
    "to.incumbs": "donations_to_incumbents",
    "to.open.seat": "donations_to_open_seats",
    "to.challs": "donations_to_challengers",
    "to.winner": "donations_to_winners",
    "to.losers": "donations_to_losers"
})

# Standardize company names to title case
df["company_name"] = df["company_name"].str.title()

# Remove unnecessary columns
# df = df.drop(columns=["person_id"])
# Convert industry names to numeric labels using LabelEncoder
le = LabelEncoder()
df['company_industry'] = le.fit_transform(df['company_industry'])
industry_mapping = dict(zip(le.classes_, le.transform(le.classes_)))

# Print mapping of original industry names to numeric labels
print(industry_mapping)
# Save the cleaned data to a new CSV file
df.to_csv("cleaned_data.csv", index=False)
# Create scatter plot of industry vs. total donations
plt.scatter(df['company_industry'], df['total_donations'])
plt.xlabel('Industry')
plt.ylabel('Total Donations')
plt.title('Industry vs. Total Donations')

plt.xticks(rotation=90, fontsize=12)  # increase x-axis label font size
plt.yticks(fontsize=12)  # increase y-axis label font size

plt.figure(figsize=(100, 100))
plt.savefig('industry_donations_scatter.png')
# Group the data by company and sum the total donations to Dems and Reps
totals = df.groupby("company_name")[
    ["total_dem_donations", "total_rep_donations"]].sum()

# Create a grouped bar chart of total donations to Dems and Reps by company
totals.plot(kind="bar", figsize=(100, 40), color=[dem_color, rep_color])

# Add labels and title
plt.xlabel("Company Name")
plt.ylabel("Total Donations")
plt.title("Total Donations to Democrats and Republicans by Company")

plt.xticks(rotation=90, fontsize=12)  # increase x-axis label font size
plt.yticks(fontsize=12)  # increase y-axis label font size
# Remove borders
plt.gca().spines["top"].set_visible(False)
plt.gca().spines["right"].set_visible(False)

# Add gridlines
plt.grid(axis="y")
# Save the plot as a PNG file
plt.savefig("dem_rep_donations_bar_chart.png", dpi=300)

# Show the plot
plt.show()
