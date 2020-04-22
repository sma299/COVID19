# this is the main python file that will conduct all of my CSV operations

# import statements
import os
import datetime
import csv
import urllib.request
from dotenv import load_dotenv

load_dotenv()

# get the date
today = datetime.datetime.today()

# intro to the system
print("WELCOME TO THE COVID-19 COUNTY TRACKER.")
print("REQUEST AT: " + today.strftime("%Y-%m-%d %I:%M %p"))
print("---------------------------------------")

# ask user to input a state and county (the result will be a string)
state_input = input("Please input your state here (ex. California): ")
county_input = input("Please input your county here (ex. Mercer): ") 

# this is the url that contains all of the county information
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# use the urllib.request (more information here: https://docs.python.org/3/howto/urllib2.html)
response = urllib.request.urlopen(url)
data = response.read()

# using the nytdata in data folder to store information
file_name = os.path.join(os.path.dirname(__file__),"..", "data", "nytdata.csv")

# write the data to a file
with open(file_name, 'wb') as f:
    f.write(data)

# define total_deaths as an integer
total_deaths = 0
deaths_array = []
cases_array = []

# parse through that data using the CSV module
# headings ['date', 'county', 'state', 'fips', 'cases', 'deaths']
with open(file_name, 'r') as f2:
    csv_file_reader = csv.DictReader(f2)
    for row in csv_file_reader:
        if row["county"] == county_input and row["state"] == state_input:
            total_deaths = total_deaths + int(row["deaths"]) # this will calculate total deaths
            new_cases = row["cases"] # most recent
            new_deaths = row["deaths"] # most recent death count 
            recent_date = row["date"] # find the most recent date
            deaths_array.append(int(new_deaths)) 
            cases_array.append(int(new_cases))

# output message with summary of data
print(f"As of " + recent_date + ", " + county_input + " County has had " + new_deaths + " new deaths due to COVID-19")
print(f"The brings the total number of deaths in " + county_input + " County to " + str(total_deaths))


len_deaths = len(deaths_array) - 1
two_weeks_deaths = deaths_array[len_deaths - 14]

len_cases = len(cases_array) - 1
two_weeks_cases = cases_array[len_cases - 14]


