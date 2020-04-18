# this is the main python file that will conduct all of my CSV operations

# import statements
import csv
import urllib2

# this is the url that contains all of the county information
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# urllib2 function (more information here: https://docs.python.org/2/library/urllib2.html)
response = urllib2.urlopen(url)
csv_reader = csv.reader(response)

for row in csv_reader:
    print row
