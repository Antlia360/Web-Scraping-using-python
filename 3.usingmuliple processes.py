import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}


def getData(url):
    response = requests.get(url, headers=headers)
    #convert to text string and return 
    #print(response.status_code)
    return response.text
    

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur,con

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
cursor, con = createDatabaseConnect(dbName)

## Now you can create Table and insert/select records from there
## Lets create a Table "summerolympics" with three columns Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation  to insert the structured data 
## we fecthed earlier

query = "CREATE TABLE IF NOT EXISTS SummerOlympics(Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation,  DONE_OR_NOT_DONE )"
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
    	if 1968 <= int(year) <= 2020 and len(url_table)<10:
    		url_table.append({'Year': year, 'Wiki_URL': 'https://en.wikipedia.org'+ wiki_url})

#use random.sample for random sampling
#random = random.sample(url_table, 2)
#print(random)
#url_selected=[
 #   'https://en.wikipedia.org'+random[0]['Wiki_URL'],
 #   'https://en.wikipedia.org'+random[1]['Wiki_URL']
#]

#For each of the pages of your two selected summer olympics, extract the data
#Name, WikipediaURL, Year, HostCity, ParticipatingNations, Atheletes, Sports, Rank_1_nation, Rank_2_nation, Rank_3_nation

#print(url_table)
for i in url_table:
    html_doc = getData(i['Wiki_URL'])
    soup = BeautifulSoup(html_doc, 'html.parser')
    Name = soup.find('span', {'class': 'mw-page-title-main'}).text   
    #print(Name)
    WikipediaURL=i['Wiki_URL']
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

       # Extracting the top 3 nations by medals
    medal_table = soup.find('table', {'class': 'plainrowheaders'})
    nations = medal_table.find_all('tr')

    rank_1_nation = nations[1].find('th').find('a').text.strip()
   # print(rank_1_nation)
    rank_2_nation = nations[2].find('th').find('a').text.strip()
   # print(rank_2_nation)
    rank_3_nation = nations[3].find('th').find('a').text.strip()
   # print(rank_3_nation)
   
   
    
    #inserting values in the table named  SummerOlympics
    query = "INSERT INTO SummerOlympics VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%d')"%(Name, WikipediaURL, Year, HostCity, count_lst_participants_cnt, Atheletes,Sports, rank_1_nation,rank_2_nation,rank_3_nation, 0)
    cursor.execute(query)
    con.commit()
    

#Now the handler code will spawn three processes using os.system call.

for _ in range(3):
    os.system("python3 scraper.py&")


