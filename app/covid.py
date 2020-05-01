# this is the main python file that will conduct all of my CSV operations

# import statements
import os
import datetime
import csv
import urllib.request

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
print(f"The brings the total number of deaths in " + county_input + " County to " + str(total_deaths))
print("---------------------------------------")


# find the length of the arrays and two-week extremes
len_deaths = len(deaths_array)
two_weeks_deaths = deaths_array[len_deaths - 15]

len_cases = len(cases_array)
two_weeks_cases = cases_array[len_cases - 15]

percent_cases = (two_weeks_cases - int(new_cases))/two_weeks_cases
percent_deaths = (two_weeks_deaths - int(new_deaths))/two_weeks_deaths

# find the average of deaths and cases over the 14-day period
i = 1
loop_deaths = 0
loop_cases = 0
percent_increase = 0
percent_decrease = 0

# while loop to add values from the array to a number that can be divided to find the average
while i < 15:
    loop_deaths = loop_deaths + deaths_array[len_deaths - i]
    loop_cases = loop_cases + cases_array[len_cases - i]
    i = i + 1

# those averages are...
average_deaths = round(loop_deaths/14,2)
average_cases = round(loop_cases/14,2)

print(f"Two weeks ago, the number of deaths in " + county_input + " County was " + str(two_weeks_deaths))
print(f"The average number of deaths over these two weeks is " + str(average_deaths))
print("---------------------------------------")

if average_deaths > int(new_deaths):
    percent_decrease = average_deaths - int(new_deaths)
    percent_decrease = percent_decrease/average_deaths
    percent_decrease = percent_decrease * 100
    percent_decrease = round(percent_decrease, 2)
    print(f"Fortunately, this means that deaths have decreased by " + str(percent_decrease) + " percent")
else:
    percent_increase = int(new_deaths) - average_deaths
    percent_increase = percent_increase/average_deaths
    percent_increase = percent_increase * 100
    percent_increase = round(percent_increase, 2)
    print(f"Unfortunately, this means that deaths have increased by " + str(percent_increase) + " percent")