# Quotes-scraper

## Project Overview

This project aims to develop a web scraper that extracts quotes from a website and saves them in a CSV file, which is then uploaded to a PostgreSQL database.

## Setup and Prerequisites

To run the script successfully, certain dependencies must be installed:
- requests
- BeautifulSoup
- psycopg2

These can be installed by running the command:
```console
pip install -r requirements.txt
```
In addition, it is necessary to set up a PostgreSQL database and insert the appropriate credentials into the script.

## Architecture Design

The web scraper uses the requests library to obtain the HTML content of the website, which is then parsed using the BeautifulSoup library to extract the quotes. The quotes are subsequently stored in a CSV file and uploaded to a PostgreSQL database using the psycopg2 library.

## Output

![Output](https://github.com/kojoh/Quotes-scraper/blob/main/images/Output.PNG)



## Improvements

- Enhance error handling in situations where the website or database is unavailable.
- Schedule the script to run periodically with a scheduler such as cron or Airflow to automate the data collection process.
