# this is the main python file that will conduct all of my CSV operations

# import statements
import os
from datetime import date
import csv
import urllib.request

# get the date
today = date.today() 

# intro to the system
print("WELCOME TO THE COVID-19 COUNTY TRACKER.")
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

# parse through that data using the CSV module
# headings ['date', 'county', 'state', 'fips', 'cases', 'deaths']
with open(file_name, 'r') as f2:
    csv_file_reader = csv.DictReader(f2)
    for row in csv_file_reader:
        if row["county"] == county_input:
            total_deaths = total_deaths + int(row["deaths"]) 
            new_deaths = row["deaths"]
            recent_date = row["date"]
    
print(f"As of " + recent_date + ", " + county_input + " County has had " + new_deaths + " new deaths")
print(f"The brings the total number of deaths in " + county_input + " County to " + str(total_deaths))
        



