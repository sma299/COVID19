# this is the main python file that will conduct all of my CSV operations

# import statements
import os
import datetime
import csv
import urllib.request
from dotenv import load_dotenv

#from app import APP_ENV

load_dotenv()

# get the date
today = datetime.datetime.today()

# intro to the system
print("WELCOME TO THE COVID-19 COUNTY TRACKER.")
print("REQUEST AT: " + today.strftime("%Y-%m-%d %I:%M %p"))
print("---------------------------------------")

#TODO: add in data validation

# ask user to input a state and county (the result will be a string)
state_input = input("Please input your state here (ex. California): ")
county_input = input("Please input your county here (ex. Mercer): ") 
print("---------------------------------------")

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

# define variables and arrays
total_deaths = 0
total_cases = 0
deaths_array = []
cases_array = []
states_array = []
counties_array = []

# parse through that data using the CSV module
# headings ['date', 'county', 'state', 'fips', 'cases', 'deaths']
with open(file_name, 'r') as f2:
    csv_file_reader = csv.DictReader(f2)
    for row in csv_file_reader:
        if row["county"] == county_input and row["state"] == state_input:
            total_deaths = total_deaths + int(row["deaths"]) # calculate totals
            total_cases = total_cases + int(row["cases"]) 
            new_cases = row["cases"] # most recent case count
            new_deaths = row["deaths"] # most recent death count 
            recent_date = row["date"] # most recent date the CSV file has been updated for that county
            deaths_array.append(int(new_deaths)) # append to arrays
            cases_array.append(int(new_cases))

# output message with summary of data
print(f"As of " + recent_date + ", " + county_input + " County has had " + new_deaths + " new deaths due to COVID-19")
print(f"Also, the number of new cases is " + new_cases + " cases")
print("---------------------------------------")
print(f"Total number of deaths: "+ str(total_deaths))
print(f"Total number of cases: " + str(total_cases))
print("---------------------------------------")


# find the length of the arrays
len_deaths = len(deaths_array)
len_cases = len(cases_array)

# find the average of deaths and cases over the 14-day period
i = 1
loop_deaths = 0
loop_cases = 0
percent_deaths = 0
percent_cases = 0

# while loop to add values from the array to a number that can be divided to find the average
while i < 15:
    loop_deaths = loop_deaths + deaths_array[len_deaths - i]
    loop_cases = loop_cases + cases_array[len_cases - i]
    i = i + 1

# those averages are...
average_deaths = round(loop_deaths/14,2)
average_cases = round(loop_cases/14,2)

print(f"The average number of deaths over these two weeks is " + str(average_deaths))
print(f"The average number of cases is " + str(average_cases))
print("---------------------------------------")

# if statement to determine if percent of deaths has increased or decreased
if average_deaths > int(new_deaths):
    percent_deaths = average_deaths - int(new_deaths)
    percent_deaths = percent_deaths/average_deaths
    percent_deaths = percent_deaths * 100
    percent_deaths = round(percent_deaths, 2)
    print(f"Fortunately, this means that deaths have decreased by " + str(percent_deaths) + " percent")
else:
    percent_deaths = int(new_deaths) - average_deaths
    percent_deaths = percent_deaths/average_deaths
    percent_deaths = percent_deaths * 100
    percent_deaths = round(percent_deaths, 2)
    print(f"Unfortunately, this means that deaths have increased by " + str(percent_deaths) + " percent")

# if statement to determine if percent of cases has increased or decreased
if average_cases > int(new_cases):
    percent_cases = average_cases - int(new_cases)
    percent_cases = percent_cases/average_cases
    percent_cases = percent_cases * 100
    percent_cases = round(percent_cases, 2)
    print(f"Cases have decreased by " + str(percent_cases) + " percent")
else:
    percent_cases = int(new_cases) - average_cases
    percent_cases = percent_cases/average_cases
    percent_cases = percent_cases * 100
    percent_cases = round(percent_cases, 2)
    print(f"Cases have increased by " + str(percent_cases) + " percent")

# print a final goodbye message
print("---------------------------------------")
print("Thank you for using the COVID-19 County Tracker")
