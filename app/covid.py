# this is the main python file that will conduct all of my CSV operations

# import statements
import os
import datetime
import csv
import urllib.request
import pandas as pd

# this is the url that contains all of the county information
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# use the urllib.request (more information here: https://docs.python.org/3/howto/urllib2.html)
response = urllib.request.urlopen(url)
data = response.read()

# using the nytdata in data folder to store information
file_name = os.path.join(os.path.dirname(__file__),"..", "data", "nytdata.csv")

with open(file_name, 'wb') as f:
    f.write(data)

covid_dict = pd.read_csv(file_name)

