# TASK : collcollect information about the different summer olympics from its Wikipedia page and
#  process the data using Python's urllib3 / requests (to get data) and BeautifulSoup library (for
#  parsing/processing), and store the collected data in a SQLite database.

# STEPS :
# --  Collect the main page of SummerOlympicsWikipedia, https://en.wikipedia.org/wiki/Summer_Olympic_Games .
# --  Create a database Create aSQLite database named 'OlympicsData.db' and a table
#  named'SummerOlympics' with the respective columns
# --  Parse the html from step1 and extract the individual summer olympics wiki page urls for
#  random 2 olympics from the last 50 years, i.e., from 1968 to 2020.
# --  For each of the pages of your two selected summerolympics, extract the data (with the help
#  of BeautifulSoup) mentioned in step 2 and insert in the database


import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


def getData(url):
    response = requests.get(url, headers=headers)
    #convert to text string and return 
    return response.text

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur

###########################################################################

# We will call https://cse.iitkgp.ac.in/~mainack/computing-lab/web-scraping/json.php
# Lets see what it returns
url = 'https://en.wikipedia.org/wiki/Summer_Olympic_Games'
html_doc = getData(url)
## it will print 
## <html>
## ...
## which in unstructured data, cannot be converted into json :( 
## bs4 to the rescue
## see the documentation here:
soup = BeautifulSoup(html_doc, 'html.parser')  
## Now bs4 will do the job for you
## Say we want to find all text within h1 tags

#Database creation
dbName = "OlympicsData.db"
cursor = createDatabaseConnect(dbName)

## Now you can create Table and insert/select records from there
## Lets create a Table "summerolympics" with three columns Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation  to insert the structured data 
## we fecthed earlier

query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation )"
cursor.execute(query)

#find list of summer olympics
list_summer_olympics = soup.find_all('table', attrs= {'class':'sortable'})
#print(len(list_summer_olympics))
url_table = []
#print(list_summer_olympics )

# Iterate through the rows of the table 
rows = list_summer_olympics[1].find_all('tr')[2:]
for row in rows:
    columns = row.find_all('td')
    if(len(columns)>=4):
    	wiki_url = columns[1].find('a')['href']
    	year=wiki_url.split('/')[2].split('_')[0]
    	#year from 1968 to 2020 filter
    	if 1968 <= int(year) <= 2020:
    		url_table.append({'Year': year, 'Wiki_URL': wiki_url})

#use random.sample for random sampling
random = random.sample(url_table, 2)
#print(random)
url_selected=[
    'https://en.wikipedia.org'+random[0]['Wiki_URL'],
    'https://en.wikipedia.org'+random[1]['Wiki_URL']
]

#For each of the pages of your two selected summer olympics, extract the data
#Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation

for i in url_selected:
    html_doc = getData(i)
    soup = BeautifulSoup(html_doc, 'html.parser')
    Name = soup.find('span', {'class': 'mw-page-title-main'}).text   
    #print(Name)
    WikipediaURL=i
    #print(WikipediaURL)
    Year=Name.split()[0] 
    #print(Year)
    HostCity= soup.find('th', text='Host city').find_next('td').text.strip().split(',')[0]
    #print(HostCity)
    count_lst_participants_cnt = soup.find('th', text='Nations').find_next('td').text.strip()
    Atheletes = soup.find('th', text='Athletes').find_next('td').text.split()[0].replace(',', '')
    #print(Atheletes)
    Sports = soup.find('th', text='Events').find_next('td').text.split()[0]
   # print(Sports)

       # Extracting the top 3 nations by medals (customize as needed)
    medal_table = soup.find('table', {'class': 'plainrowheaders'})
    nations = medal_table.find_all('tr')

    rank_1_nation = nations[1].find('th').find('a').text.strip()
   # print(rank_1_nation)
    rank_2_nation = nations[2].find('th').find('a').text.strip()
   # print(rank_2_nation)
    rank_3_nation = nations[3].find('th').find('a').text.strip()
   # print(rank_3_nation)
    
    #inserting values in the table named  city_weather
    query = "INSERT INTO SummerOlympics VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(Name, WikipediaURL, Year, HostCity, count_lst_participants_cnt, Atheletes,Sports, rank_1_nation,rank_2_nation,rank_3_nation  )
    cursor.execute(query)


## Lets see what is in the table
query = "SELECT DISTINCT Year FROM SummerOlympics"
result = cursor.execute(query)
years=[]
for row in result:
#prints years
	print(row[0],end=" ")
	years.append(row[0])
print()
query = "SELECT AVG(ParticipatingNations) FROM SummerOlympics"
result = cursor.execute(query)

for row in result:
#prints years
	print(row[0])
	

query = "SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation FROM SummerOlympics WHERE Year IN (?)"
result = cursor.execute(query,(years[0],))
x=set(cursor.fetchone())
query = "SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation FROM SummerOlympics WHERE Year IN (?)"
result = cursor.execute(query,(years[1],))
y=set(cursor.fetchone())

print(x.intersection(y))
cursor.close()




