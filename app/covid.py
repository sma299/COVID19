# this is the main python file that will conduct all of my CSV operations

# import statements
import os
import datetime
import csv
import urllib.request

# ask user to input a county
print("Welcome to the COVID-19 county tracker.")
print("--------------------------------------------------")

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
        if str(row["county"]) == county_input:
            print(row["deaths"])



