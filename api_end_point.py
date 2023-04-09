import csv
from flask import Flask, jsonify, render_template
import pandas as pd

# Load the cleaned data into a Pandas dataframe
df = pd.read_csv("cleaned_data.csv")

# Initialize the Flask app
app = Flask(__name__, template_folder='templates')

# Create an API endpoint to return all the data as JSON
# Define a route for the home page
# Load data into memory
data = {}
with open('cleaned_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    for row in reader:
        company_name = row[0]
        company_details = {}
        for i in range(len(header)):
            company_details[header[i]] = row[i]
        data[company_name] = company_details


@app.route('/')
def home():
    return '''
    <html>
        <head>
            <title></title>
        </head>
        <body>
            <h1>Welcome</h1>
            <p>Welcome to our website, where we provide a unique insight into the world of political donations. Our platform utilizes publicly available data to showcase the donations given to both Republican and Democratic parties by corporations.

At a time where transparency and accountability are at the forefront of political discussions, we believe it is important to provide an easily accessible and user-friendly resource for individuals to explore the funding sources of political parties. Our platform aims to bridge the gap between the public and political funding information by presenting it in a clear and concise manner.
p>
Through our website, users can easily search and browse through a comprehensive database of corporate donations made to political parties. Our platform provides users with the opportunity to explore the relationship between political parties and corporations, and how these donations may influence political decision-making.<
We believe in the power of information and transparency, and we hope that our platform can contribute to a more informed and engaged society. Join us on our mission to uncover the truth behind political funding and donations.<
            <ul>
                <li><h1><a href="/donations">Donations</a></h1></li>
            </ul>
        </body>
    </html>
    '''

# Define a route to get the donation data and display it using a template


@app.route('/donations')
def get_donations():
    data = df.groupby('company_name')['total_donations'].sum().reset_index()
    return render_template('donations.html', data=data.to_dict(orient='records'))

# Define a route to get company details by name and display them using a template


@app.route('/company/<company_name>')
def get_company_details(company_name):
    with open('cleaned_data.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            for cell in row:
                if company_name.lower() in cell.lower():
                    company_details = {}
                    for i in range(len(header)):
                        company_details[header[i]] = row[i]
                    return render_template('company.html', company_name=company_name, company_details=company_details)
    return render_template('company_not_found.html', company_name=company_name)


# Run the app
if __name__ == '__main__':
    app.run(port=4004)
