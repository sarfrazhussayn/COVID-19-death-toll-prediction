import requests
import pandas as pd
import json
import time
from datetime import datetime,timedelta
import pycountry
import tempfile
import csv
import os


countries = {}
for country in pycountry.countries:
    countries[country.alpha_3] = country.name


today = datetime.today() - timedelta(days=5) #Date range set last day where index of all countries was available
today = today.strftime('%Y-%m-%d')

# start = datetime.today() - timedelta(days=7)
# start = start.strftime('%Y-%m-%d')
# print(today)
# print(start)
# start = '2020-01-21'
# api-endpoint


# URL = "https://api.covid19api.com/all"
URL = "https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/"+str(today)+"/"+str(today)


# sending get request and saving the response as response object
r = requests.get(url = URL)

# extracting data in json format
data = r.json()

filename = 'latest_stringency.csv'

with open('temp.csv', 'w') as temp_file:
  writer = csv.writer(temp_file)

  writer.writerow(['location','stringency_index'])
  for date in data['data'].keys():
    for country in data['data'][date]:
      try:
        writer.writerow([countries[country],data['data'][date][country]['stringency']])
      except:
        pass


try:
  os.remove(filename)
except:
  pass

os.rename('temp.csv',filename)
