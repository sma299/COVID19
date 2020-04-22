# this is the main python file that will conduct all of my CSV operations

# import statements
import os
from datetime import date
import csv
import urllib.request

# get the date in order to do the calculations
today = date.today() 
print("Current day:", today.day)

# intro to the system
print("Welcome to the COVID-19 county tracker.")
print("---------------------------------------")

# ask user to input a county
county_input = input("Please input your state county here: ") #the resulting value is a string

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

# parse through that data using the CSV module
# ['date', 'county', 'state', 'fips', 'cases', 'deaths']
with open(file_name, 'r') as f2:
    csv_file_reader = csv.DictReader(f2)
    for row in csv_file_reader:
        if row["county"] == county_input:
            county_deaths = row["deaths"] 
            recent_date = row["date"]
    for entry in csv_file_reader:
        if entry["date"] == recent_date and row["county"] == county_input:
            print("Number of deaths as of " + recent_date)
        



