#Problem: To collect the weather data from an online API 
#and store it in a local SQLite database


#importing the necessary libraries
import requests     #sendingGETrequestandreceiving data
import sqlite3      # for storing data
import json         # for processing structured data that you receive back
from bs4 import BeautifulSoup     # for processing unstructured data

def getData(url):
    response = requests.get(url)
    #convert to text string and return 
    return response.text

def convertJson(data):
    return json.loads(data)

def createDatabaseConnect(dbName):
	con = sqlite3.connect(dbName)
	cur = con.cursor()
	return cur,con
	
	###########################################################################
# We will call api.openweathermap.org/data/2.5/weather?q=London,uk&APPID=35a464b4cdfb06d2be77c2bc1ac5e0e4
# Lets see what it returns
url = 'https://api.openweathermap.org/data/2.5/weather?lat=44.39&lon=10.98&appid=35a464b4cdfb06d2be77c2bc1ac5e0e4'
returnedData = getData(url)
jsonData = convertJson(returnedData)
## Now jsonData contains a python dict
#print(jsonData)

#Extarcting the details from the API responses, ie,  Cityname,
# Currenttemperature(in Kelvin), Weatherdescription, Humidity(%), windspeed(meter/sec)

City_name=jsonData['name']
Current_temperature=jsonData['main']['temp_min']
Weather_description=jsonData['weather'][0]['description']
Humidity=jsonData['main']['humidity']
Wind_speed = jsonData['wind']['speed']


#create a SQLite database named 'Weather.db'
#create a table named 'city_wether' with colums City, Temperature, Description, Humidity, WindSpeed
# Insert the extracted data into the 'city_weather' table
#create table if it doesnt exists
dbName = "Weather.db"
cursor,connection = createDatabaseConnect(dbName)
query = "CREATE TABLE IF NOT EXISTS city_weather(City, Temperature, Description, Humidity, WindSpeed)"
cursor.execute(query)

query = "INSERT INTO city_weather VALUES ('%s', '%s', '%s', '%s', '%s')"%(City_name, Current_temperature, Weather_description, Humidity, Wind_speed )
cursor.execute(query)
connection.commit()

## Printing the table 
#Lets see what is in the table
query = "SELECT * from city_weather"
result = cursor.execute(query)

for row in result:
	print(row)
cursor.close()





