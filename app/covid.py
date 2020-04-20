# this is the main python file that will conduct all of my CSV operations

# import statements
import os
import datetime
import csv
import urllib.request

# this is the url that contains all of the county information
url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"

# use the urllib.request module with the open function
response = urllib.request.urlopen(url)
data = response.read()

file_name = os.path.join(os.path.dirname(__file__),"..", "data", "nytdata.csv")

with open(file_name, 'wt') as f:
    f.write(data)

# urllib2 function (more information here: https://docs.python.org/3/howto/urllib2.html)
# with urlopen(url) as response:
   # url_text = response.read()

# with open(csv_file_path, "r") as csv_file:
#csv_dict = csv.DictReader(url_text)

#for row in csv_dict:
    #print(row)
