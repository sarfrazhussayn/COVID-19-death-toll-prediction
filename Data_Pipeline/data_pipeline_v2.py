import requests
import csv
from bs4 import BeautifulSoup
import os


# scrapes html, finds specific tag through id, finally saves all td tags. 
url = "https://www.worldometers.info/coronavirus/"
request = requests.get(url)
htmlText = request.text
soup = BeautifulSoup(htmlText, "html.parser")
data = soup.find(id="main_table_countries_today")
data = data.find_all('td')

# removes all tags and saves all text data in data_list.
data_list = []
for entries in data:
  data_list.append(entries.text.strip())

#row_length contains number of elements in a single row.
row_length = data_list.index("Brazil") - data_list.index("USA")


data_list = data_list[data_list.index("USA")::]
data_list = data_list[0:data_list.index("China") + row_length]

data_list = [0] + data_list

covid19_data = {}

for i in range(1, len(data_list), 19):
  
  covid19_data[data_list[i]] = {'total_cases':int(data_list[i+1].replace(",","")), 'total_deaths':data_list[i+3].replace(",",""), 'population':data_list[i+13].replace(",","")}

  if covid19_data[data_list[i]]['total_deaths'] != "":
    covid19_data[data_list[i]]['total_deaths'] = int(covid19_data[data_list[i]]['total_deaths'])

  if covid19_data[data_list[i]]['population'] != "":
    covid19_data[data_list[i]]['population'] = int(covid19_data[data_list[i]]['population'])

covid19_data['United States'] = covid19_data['USA']
covid19_data['United Kingdom'] = covid19_data['UK']
covid19_data['United Arab Emirates'] = covid19_data['UAE']
covid19_data['South Korea'] = covid19_data['S. Korea']
covid19_data['Czech Republic'] = covid19_data['Czechia']
covid19_data['Vatican'] = covid19_data['Vatican City']



filename = 'AggregatedData_v1.csv'
f = open(filename)
reader = csv.reader(f)

#creates a temporary file to save updated data.
with open('temp.csv', 'w', newline='') as temp_file:
  writer = csv.writer(temp_file)

  for row in reader:
    if row[0] == 'location':
      writer.writerow(row)
    else:
      try:
        new_row = [row[0]] + [covid19_data[row[0]]['total_cases']] + [covid19_data[row[0]]['total_deaths']] + [row[3]] + [covid19_data[row[0]]['population']] + row[5::]
        writer.writerow(new_row)
      except:
        pass
        # print(row[0],"not in covid19_data")

f.close()
#remove the origional file.
os.remove(filename)

#rename temporary file. 
os.rename('temp.csv',filename)

