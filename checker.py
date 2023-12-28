import requests
import sqlite3
import json
from bs4 import BeautifulSoup
import random
import os


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



# Report if all the database rows are populated, i.e., there is no DONE_OR_NOT_DONE which is set to 0 and no process is working
query1="SELECT COUNT(*) FROM SummerOlympics WHERE DONE_OR_NOT_DONE = '0'"
cursor.execute(query1)
remaining_rows = cursor.fetchone()[0]

# If all rows are populated, print answers to the questions
if remaining_rows == 0:
    # What are the years you chose?
    cursor.execute("SELECT DISTINCT Year FROM SummerOlympics")
    chosen_years = [row[0] for row in cursor.fetchall()]
    print("The years you chose?:", chosen_years)

    #Which country was within the top 3 for the maximum time in your database?
    cursor.execute("SELECT Rank_1_nation, Rank_2_nation, Rank_3_nation FROM SummerOlympics")
    rank_counts = {}
    for row in cursor.fetchall():
        for rank in row:
            if rank in rank_counts:
                rank_counts[rank] += 1
            else:
                rank_counts[rank] = 1
    top_3_countries = sorted(rank_counts, key=rank_counts.get, reverse=True)[:3]
    print("top 3 for the maximum time:", top_3_countries)

    #What is the average number of athletes?
    cursor.execute("SELECT AVG(Athletes) FROM SummerOlympics")
    average_athletes = cursor.fetchone()[0]
    print("Average Number of Athletes:", average_athletes)


con.close()
