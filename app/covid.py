# this is the main python file that will conduct all of my CSV operations

# import statements

import os 
from datetime import date # to get the date for the email
import csv # to process the csv file
import urllib.request # to open the URL (could also use the requests package)
from dotenv import load_dotenv # to load the env file and get encrypted info
from app import APP_ENV 
from app.email_service import send_email # use the sendgrid package to send email

# help to load all of the .env info
load_dotenv()

# encrypted info and the defaults
STATE = os.getenv("STATE", default="California")
COUNTY = os.getenv("COUNTRY_CODE", default="Orange")
MY_NAME = os.getenv("MY_NAME", default="Hottest Person in the World")

def get_data():
    """
    WHAT IT DOES: This function gathers the data from the NYTimes County Database

    PARAMETERS: N/A

    RETURNS: Returns a CSV filename that can be used in conjunction with the DictReader function
    """
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

    return file_name

def string_validation(state_input, county_input):
    """
    WHAT IT DOES: Processes the State and County variables to ensure that they are strings

    PARAMETERS: N/A

    RETURNS: A message string with any errors
    """
    message = " "

    while True:
        try:
            STATE = str(state_input)
            COUNTY = str(county_input)
            break
        except ValueError:
            message += "ERROR: Your input cannot be an integer"
    
    return message


def data_validation(state_input, county_input, states_array, counties_array):
    """
    WHAT IT DOES: Processes the State and County variables to ensure that they actually exist

    PARAMETERS: two strings, two arrays of string variables

    RETURNS: A boolean
    """
    found_it = False
    i = len(states_array) - 1

    if state_input in states_array and county_input in counties_array:
        while i >= 0 and found_it == False:
            if states_array[i] == state_input and counties_array[i] == county_input:
                found_it = True
            i = i - 1

    return found_it


def average_deaths(deaths_array):
    """
    WHAT IT DOES: Averages out the number of deaths over the last 14 days

    PARAMETERS: An deaths array of integers

    RETURNS: An integer of the average amount of deaths
    """
    len_deaths = len(deaths_array)
    i = 1
    loop_deaths = 0
    while i < 15:
        loop_deaths = loop_deaths + deaths_array[len_deaths - i]
        i = i + 1
    average_deaths = round(loop_deaths/14,2)

    return average_deaths

def average_cases(cases_array):
    """
    WHAT IT DOES: Averages out the number of cases over the last 14 days

    PARAMETERS: A cases array of integers

    RETURNS: An integer of the average amount of cases
    """
    len_cases = len(cases_array)
    i = 1
    loop_cases = 0
    while i < 15:
        loop_cases = loop_cases + cases_array[len_cases - i]
        i = i + 1
    average_cases = round(loop_cases/14,2)

    return average_cases

def deaths_change(average_deaths, new_deaths):
    """
    WHAT IT DOES: Calculates if the newest number of deaths is less than or greater than the average deaths over 14 days

    PARAMETERS: An average deaths integer, a new deaths integer

    RETURNS: A string message with the percent increase or decrease of deaths
    """
    percent_deaths = 0
    message = " "
    
    # if statement to determine if percent of deaths has increased or decreased
    if average_deaths > int(new_deaths):
        percent_deaths = average_deaths - int(new_deaths)
        percent_deaths = percent_deaths/average_deaths
        percent_deaths = percent_deaths * 100
        percent_deaths = round(percent_deaths, 2)
        message += "Fortunately, this means that deaths have decreased by " + str(percent_deaths) + " percent"
    else:
        percent_deaths = int(new_deaths) - average_deaths
        percent_deaths = percent_deaths/average_deaths
        percent_deaths = percent_deaths * 100
        percent_deaths = round(percent_deaths, 2)
        message += "\nUnfortunately, this means that deaths have increased by " + str(percent_deaths) + " percent"

    return message

def cases_change(average_cases, new_cases):
    """
    WHAT IT DOES: Calculates if the newest number of deaths is less than or greater than the average deaths over 14 days.

    PARAMETERS: An average deaths integer, a new deaths integer

    RETURNS: A string message with the percent increase or decrease of deaths
    """

    percent_cases = 0
    message = " "

    # if statement to determine if percent of cases has increased or decreased
    if average_cases > int(new_cases):
        percent_cases = average_cases - int(new_cases)
        percent_cases = percent_cases/average_cases
        percent_cases = percent_cases * 100
        percent_cases = round(percent_cases, 2)
        message += "Cases have decreased by " + str(percent_cases) + " percent"
    else:
        percent_cases = int(new_cases) - average_cases
        percent_cases = percent_cases/average_cases
        percent_cases = percent_cases * 100
        percent_cases = round(percent_cases, 2)
        message += "Cases have increased by " + str(percent_cases) + " percent"
    
    return message


if __name__ == "__main__":

    # should the state/county be input or default? If in development, then input
    if APP_ENV == "development":
        state_input = input("PLEASE INPUT A STATE (e.g. California): ")
        county_input = input("PLEASE INPUT A COUNTY (e.g. Orange): ")
        string_validation(state_input, county_input)
    else:
        state_input = STATE
        county_input = COUNTY

    # define variables and arrays
    total_deaths = 0 # int
    total_cases = 0 # int
    deaths_array = [] # array of ints
    cases_array = [] # array of ints
    states_array = []  # array of strings
    counties_array = [] # array of strings

    # parse through that data using the CSV module
    # headings ['date', 'county', 'state', 'fips', 'cases', 'deaths']
    with open(get_data(), 'r') as f2:
        csv_file_reader = csv.DictReader(f2)
        for row in csv_file_reader:
            states_array.append(row["state"]) 
            counties_array.append(row["county"]) 
            if row["county"] == county_input and row["state"] == state_input:
                total_deaths = total_deaths + int(row["deaths"]) # int
                total_cases = total_cases + int(row["cases"]) # int
                new_deaths = row["deaths"] # string, most recent death count
                new_cases = row["cases"] # string, most recent case count
                recent_date = row["date"] # string, most recent date the CSV file has been updated for that county
                deaths_array.append(int(new_deaths))
                cases_array.append(int(new_cases))

    # data validation to make sure the state and county exist!
    if data_validation(state_input, county_input, states_array, counties_array) == True:
            
        # start the email
        html = ""
        html += f"<h3>Good Morning, {MY_NAME}!</h3>"

        html += "<h4>Today's Date</h4>"
        html += f"<p>{date.today().strftime('%A, %B %d, %Y')}</p>"

        html += f"<h4>COVID-19 COUNTY STATISTICS for {county_input} County, {state_input}:</h4>"

        # output message with summary of data
        html += f"<p>As of {recent_date}, {county_input} County has had {new_deaths} new deaths due to COVID-19<p>"
        html += f"<p>Also, the number of new cases in {county_input} County is {new_cases}<p>"
        html += f"<h4>---------------------------------------</h4>"

        html += "</ul>"
        html += f"<li>Total number of deaths: {str(total_deaths)}</li>"
        html += f"<li>Total number of cases: {str(total_cases)}</li>"
        html += f"<li>Average number of deaths over two weeks: {average_deaths(deaths_array)}</li>"
        html += f"<li>Average number of cases over two weeks: {average_cases(cases_array)}</li>"
        html += "</ul>"

        html += f"<h4>---------------------------------------</h4>"

        html += f"<p>{deaths_change(average_deaths(deaths_array), new_deaths)}<p>"
        html += f"<p>{cases_change(average_cases(cases_array), new_cases)}<p>"

        # print a final goodbye message
        html += "<h3>Thank you for using the COVID-19 County Tracker.</h3>"

        # send the email
        send_email(subject="COVID-19 Daily County Report", html=html)

    else: # error message
        print("Unfortunately, that state and county combination does not exist in our database. Please try again.")