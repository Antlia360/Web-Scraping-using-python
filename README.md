## Web Scraping with Python

Introduces you to web scraping using Python, where you'll learn to collect data from websites, parse it, and store it for further analysis. We'll cover the basic architecture of a scraper and utilize various Python libraries for different tasks.

### Setting Up Your Environment

Before diving into the implementation, make sure you have the following libraries installed:

- `requests` or `urllib3`: For sending GET requests and receiving data.
- `json`: For processing structured data.
- `beautifulsoup4` (bs4): For parsing and processing unstructured data.
- `sqlite3`: For storing data in a local SQLite database.
- `random`: For random sampling.

You can install these libraries using the following command: `pip3 install <libraryname>`

### 1: Collecting and Storing Structured JSON Data

In this problem, you'll collect weather data from the OpenWeatherMap API and store it in a local SQLite database. Follow these steps:
1. Make API calls to the OpenWeatherMap API using your API key.
2. Extract relevant information from the API response, such as city name, temperature, weather description, humidity, and wind speed.
3. Create a SQLite database named `Weather.db` and a table named `city_weather` to store the extracted data.
4. Insert the extracted data into the `city_weather` table.
5. Test your system with three to five different cities of your choice, included in a test function

Done `weather_data.py`

### 2: Collecting, Storing, and Processing Unstructured Data

This problem involves collecting information about Summer Olympics from its Wikipedia page, processing the data, and storing it in a SQLite database. Here's what you need to do:
1. **Collect Wikipedia Page:** Collect the main page of Summer Olympics Wikipedia from [here](https://en.wikipedia.org/wiki/Summer_Olympic_Games). You may need to use headers for fetching this page.

2. **SQLite Database:** Create a SQLite database named `OlympicsData.db` and a table named `SummerOlympics` with the following columns:
   - Name (e.g. “2012 Summer Olympics”, in title of respective Wikipedia pages)
   - WikipediaURL
   - Year (the year when it's conducted)
   - HostCity (the city where it's hosted)
   - ParticipatingNations (List of the participating nations)
   - Athletes (number of athletes)
   - Sports (list of sports)
   - Rank_1_nation
   - Rank_2_nation
   - Rank_3_nation

3. **Parse HTML and Extract URLs:** Parse the HTML from step 1 and extract the individual Summer Olympics wiki page URLs for random 2 Olympics from the last 50 years (i.e., from 1968 to 2020). You can try parsing the “List of Summer Olympic Games” table to get the URLs and use `random.sample` for random sampling.

4. **Extract Data and Insert into Database:** For each of the pages of your two selected Summer Olympics, extract the data using `BeautifulSoup` mentioned in step 2 and insert it into the database.

5. **Data Analysis:** Using the database, print answers to the following questions:
   - What are the years you chose?
   - What is the average number of countries participating in the two Olympics?
   - Print the overlap (i.e., common nations) within <Rank_1_nation, Rank_2_nation, and Rank_3_nation> for your chosen two years.

Done in `unstructured data.py`

### 3: Using Multiple Processes for Speed Up

In this task, we will enhance the data collection process by utilizing multiple processes for speed up. The goal is to collect information about different Summer Olympics from Wikipedia pages and store the data in a SQLite database.

## Task Description

1. **Handler Function:** Write a handler function that performs the following tasks:
   - Collect the main page of Summer Olympics Wikipedia.
   - Create a SQLite database named 'OlympicsData.db' and a table named 'SummerOlympics' with the specified columns.
   - Parse the HTML to extract the individual Summer Olympics wiki page URLs for ten Olympics from the last 50 years, i.e., from 1968 to 2020.
   - Insert the Wikipedia URLs into the database and set the 'DONE_OR_NOT_DONE' flag as 0 for all rows.

Done in `muliple processes.py`

2. **Spawn Processes:** The handler code will spawn three processes using the `os.system` call to run the scraper script concurrently.

Example of this call
`import os
os.system(“python3 scraper.py&”)`
This will run “python3 scraper.py” in a separate process.

3. **Scraper Script (scraper.py):** This script will perform the following tasks:
   - Check the database for rows where the 'DONE_OR_NOT_DONE' flag is 0.
   - Pick a row where 'DONE_OR_NOT_DONE' is 0. If no such row exists, the script will exit.
   - Set the 'DONE_OR_NOT_DONE' flag to 1 for the chosen row.
   - Fetch the Wikipedia page using the URL in the 'WikipediaURL' column.
   - Parse the page using BeautifulSoup and populate the corresponding columns in the database.

4. **Checker Script (checker.py):** This script will check the database and:
   - Report if all the database rows are populated (i.e., 'DONE_OR_NOT_DONE' is set to 0 and no process is working).
   - If all database rows are populated, print answers to the specified questions.
   -   i. What are the years you chose?
   -   ii. Which country was within top 3 for the maximum time in your database?
   -   iii. What is the average number of athletes?

## Implementation

Here's a high-level overview of the implementation:

1. Write the handler function to perform the initial setup, database creation, and URL extraction.
2. Implement the scraper script to fetch and parse Wikipedia pages concurrently using multiple processes.
3. Develop the checker script to monitor the database and report completion status.
4. Execute the handler function to initiate the data collection process.
5. Run the scraper script in parallel processes to fetch and process Wikipedia pages.
6. Use the checker script to ensure that all data has been collected and perform any final analysis or reporting.

