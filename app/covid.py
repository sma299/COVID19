# COVID-19 County Tracker

##
## Module & Package Import
##

import os 
from datetime import date # to get the date for the email
import csv # to process the csv file
import urllib.request # to open the URL (could also use the requests package)
from dotenv import load_dotenv # to load the env file and get encrypted info
from app import APP_ENV 
from app.email_service import send_email # use the sendgrid package to send email

import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go

##
## Get Environment Variables
##

load_dotenv()

STATE = os.getenv("STATE", default="California")
COUNTY = os.getenv("COUNTRY_CODE", default="Orange")
MY_NAME = os.getenv("MY_NAME", default="Hottest Person in the World")

# plotly credential setup
PLOTLY_USER_NAME = os.environ.get("PLOTLY_USER_NAME")
PLOTLY_API_KEY = os.environ.get("PLOTLY_API_KEY")

chart_studio.tools.set_credentials_file(username=PLOTLY_USER_NAME, api_key=PLOTLY_API_KEY)


##
## Begin Functions 
##

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

def string_validation(state_input, county_input):
    """
    WHAT IT DOES: Processes the State and County variables to ensure that they are strings

    PARAMETERS: Two strings representing a state and county in the US

    RETURNS: A boolean
    """
    has_errors = False

    try:
        int_variable = int(state_input)
        int_variable2 = int(county_input)
        has_errors = True
    except:
        pass

    return has_errors


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
    average_deaths = round(loop_deaths/14,0)

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
    average_cases = round(loop_cases/14,0)

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
    if average_deaths > new_deaths:
        percent_deaths = average_deaths - new_deaths
        percent_deaths = percent_deaths/average_deaths
        percent_deaths = percent_deaths * 100
        percent_deaths = round(percent_deaths, 2)
        message += "Fortunately, this means that deaths have decreased by " + str(percent_deaths) + "% below the two-week average."
    else:
        percent_deaths = int(new_deaths) - average_deaths
        percent_deaths = percent_deaths/average_deaths
        percent_deaths = percent_deaths * 100
        percent_deaths = round(percent_deaths, 2)
        message += "\nUnfortunately, this means that deaths have increased by " + str(percent_deaths) + "% above the two-week average."

    return message

def cases_change(average_cases, new_cases):
    """
    WHAT IT DOES: Calculates if the newest number of cases is less than or greater than the average cases over 14 days.

    PARAMETERS: An average cases integer, a new cases integer

    RETURNS: A string message with the percent increase or decrease of cases
    """

    percent_cases = 0
    message = " "

    # if statement to determine if percent of cases has increased or decreased
    if average_cases > new_cases:
        percent_cases = average_cases - new_cases
        percent_cases = percent_cases/average_cases
        percent_cases = percent_cases * 100
        percent_cases = round(percent_cases, 2)
        message += "Cases have decreased by " + str(percent_cases) + "% below the average."
    else:
        percent_cases = new_cases - average_cases
        percent_cases = percent_cases/average_cases
        percent_cases = percent_cases * 100
        percent_cases = round(percent_cases, 2)
        message += "Cases have increased by " + str(percent_cases) + "% above the average."
    
    return message

def formatting(amount):
    """
    WHAT IT DOES: this function turns a number into standard comma notation

    PARAMETERS: passes in a number

    RETURNS: a formatted number string (ex. 5,350.99)
    """
    return "{:,}".format(amount)

##
## If Name == Main
##

if __name__ == "__main__":

    get_data()

    # should the state/county be input or default? If in development, then input
    if APP_ENV == "development":
        state_input = input("PLEASE INPUT A STATE (e.g. California): ")
        county_input = input("PLEASE INPUT A COUNTY (e.g. Orange): ")
    else:
        state_input = STATE
        county_input = COUNTY
    
    if string_validation(state_input, county_input) == False:

        # define variables and arrays
        total_deaths = 0 # int
        total_cases = 0 # int
        new_deaths = 0 # int
        new_cases = 0 # int
        deaths_array = [] # array of ints
        cases_array = [] # array of ints
        states_array = []  # array of strings
        counties_array = [] # array of strings
        file_path = os.path.join(os.path.dirname(__file__),"..", "data", "nytdata.csv")

        # parse through that data using the CSV module
        # headings ['date', 'county', 'state', 'fips', 'cases', 'deaths']
        with open(file_path, 'r') as f2:
            csv_file_reader = csv.DictReader(f2)
            for row in csv_file_reader:
                states_array.append(row["state"]) 
                counties_array.append(row["county"]) 
                if row["county"] == county_input and row["state"] == state_input:

                    new_deaths = int(row["deaths"]) - total_deaths # used to be strings, now are integers
                    new_cases = int(row["cases"]) - total_cases # used to be strings, now are integers

                    total_deaths = int(row["deaths"]) # int, total death count
                    total_cases = int(row["cases"]) # int, total case count

                    recent_date = row["date"] # string, most recent date the CSV file has been updated for that county

                    deaths_array.append(int(new_deaths))
                    cases_array.append(int(new_cases))
    else:
        print("ERROR: your inputs cannot have integers in it! Please try again.")
        exit()
    
    # data validation to make sure the state and county exist!
    if data_validation(state_input, county_input, states_array, counties_array) == True:

        ##
        ## HTML Object for Email
        ##
            
        html = ""
        html += f"<h3>Good Morning, {MY_NAME}!</h3>"

        html += "<h4>Today's Date</h4>"
        html += f"<p>{date.today().strftime('%A, %B %d, %Y')}</p>"

        html += f"<h4>COVID-19 COUNTY STATISTICS for {county_input} County, {state_input}:</h4>"

        # output message with summary of data
        html += f"<p>As of {recent_date}, {county_input} County has had {formatting(new_deaths)} new deaths due to COVID-19.</p>"
        html += f"<p>Also, the number of new cases in {county_input} County is {formatting(new_cases)}.</p>"
        html += f"<h4>---------------------------------------</h4>"

        html += "</ul>"
        html += f"<li>Total number of deaths: {formatting(total_deaths)}</li>"
        html += f"<li>Total number of cases: {formatting(total_cases)}</li>"
        html += f"<li>Average number of deaths over two weeks: {formatting(average_deaths(deaths_array))}</li>"
        html += f"<li>Average number of cases over two weeks: {formatting(average_cases(cases_array))}</li>"
        html += "</ul>"

        html += f"<h4>---------------------------------------</h4>"

        html += f"<p>{deaths_change(average_deaths(deaths_array), new_deaths)}</p>"
        html += f"<p>{cases_change(average_cases(cases_array), new_cases)}</p>"

        # print a final goodbye message
        html += "<h3>Thank you for using the COVID-19 County Tracker.</h3>"


        # create Plotly graph HERE
        len_deaths = len(deaths_array)
        i = 1
        plotly_deaths = []
        while i < 15:
            plotly_deaths.append(deaths_array[len_cases - i])
            i = i + 1

        trace0 = go.Scatter(
        x=[14,13,12,11,10,9,8,7,6,5,4,3,2,1],
        y=plotly_deaths
        )

        data = [trace0]

        py.plot(data, filename = 'basic-line', auto_open=True)









        # send the email
        #send_email(subject="COVID-19 Daily County Report", html=html)

    else: # error message
        print("Unfortunately, that state and county combination does not exist in our database. Please try again.")

