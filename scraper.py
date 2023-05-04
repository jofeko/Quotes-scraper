import requests
from bs4 import BeautifulSoup
import csv
import psycopg2
from datetime import datetime
import os



def scrape_quotes():
    # Scrape the website
    url = "http://quotes.toscrape.com/"

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the quotes and extract the text, author, and tags
    quotes = soup.find_all('div', class_='quote')
    data = []
    for quote in quotes:
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        tags = quote.find('meta', class_='keywords')['content']
        data.append([text, author, tags])

    return data

def save_to_csv(data):
    # Save the data to a CSV file
    global filename
    filename = "quotes.csv"
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["quotes", "author", "tags"])
        writer.writerows(data)

def upload_to_postgres():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host = os.getenv('DATABASE_HOST'), 
        database = os.getenv('DATABASE_DB'), 
        user = os.getenv('DATABASE_USER'), 
        password = os.getenv('DATABASE_PASSWORD'), 
        port = os.getenv('DATABASE_PORT')
    )

    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute('''CREATE TABLE IF NOT EXISTS quotes
                 (quotes TEXT, author TEXT, tags TEXT, date TIMESTAMP)''')
    conn.commit()

    # Upload the data to PostgreSQL
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            cur.execute("INSERT INTO quotes (quotes, author, tags, date) VALUES (%s, %s, %s, %s)",
                        (row[0], row[1], row[2], datetime.now()))
            conn.commit()

    # Close the database connection
    cur.close()
    conn.close()

    print("Data scraped, saved to CSV and uploaded to PostgreSQL database successfully.")

if __name__ == '__main__':
    data = scrape_quotes()
    save_to_csv(data)
    upload_to_postgres()
