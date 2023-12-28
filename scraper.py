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
	return cur, con

###########################################################################

#Database creation
dbName = "OlympicsData.db"
cursor, con = createDatabaseConnect(dbName)

# check the database for rows where DONE_OR_NOT_DONE f lag is 0.
query1="SELECT * FROM SummerOlympics where DONE_OR_NOT_DONE='0'"
cursor.execute(query1)
row = cursor.fetchone()

#print(row)
#pick a row where DONE_OR_NOT_DONEis0(ifnosuchrow,scraper.pywill exit).
if row is None:
    con.close()
    print(row, 'bye')
    exit() 
    
query1="UPDATE SummerOlympics SET DONE_OR_NOT_DONE = ? WHERE WikipediaURL= ?"
cursor.execute(query1, ('1', row[1]))
    

html_doc = getData(row[1])
soup = BeautifulSoup(html_doc, 'html.parser')
Name = soup.find('span', {'class': 'mw-page-title-main'}).text   
    #print(Name)
WikipediaURL=row[1]
    #print(WikipediaURL)
Year=Name.split()[0] 
    #print(Year)
HostCity= soup.find('th', text='Host city').find_next('td').text.strip().split(',')[0]
    #print(HostCity)
count_lst_participants_cnt = soup.find('th',text='Nations').find_next('td').text.strip() 
Atheletes = soup.find('th',text='Athletes').find_next('td').text.split()[0].replace(',', '')
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
    
query1="UPDATE SummerOlympics set Name = ?,Year=?, HostCity=?, ParticipatingNations=?, Atheletes=?, Sports=?, Rank_1_nation=?, Rank_2_nation=?, Rank_3_nation=? where WikipediaURL = ?"
data=(Name, Year,  HostCity,  count_lst_participants_cnt, Atheletes,  Sports,  rank_1_nation, rank_2_nation, rank_3_nation, WikipediaURL)
cursor.execute(query1, data)
con.commit()
cursor.close()
#For the row chosen, scraper.py will first set the DONE_OR_NOT_DONE to 1.


 #d. Thenitwill fetch the wikipedia page using URL in the WikipediaURL column
# e. NextusingbeautifulSoup it will parse the page and populate the columns mentioned in step 1.b. corresponding row in the database
#query="INSERT INTO SummerOlympics (Name, WikipediaURL, DONE_OR_NOT_DONE) VALUES (?, ?, 0)"
#result=cursor.execute(query, (i['Name'], WikipediaURL))


os.system("python3 checker.py&")
