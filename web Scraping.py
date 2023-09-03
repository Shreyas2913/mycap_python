import requests
from bs4 import BeautifulSoup
import sqlite3

# Define the URL you want to scrape images from
url = 'https://www.flipkart.com/search?q=samsung+tv&as=on&as-show=on&otracker=AS_Query_OrganicAutoSuggest_4_3_na_na_ps&otracker1=AS_Que'  # Replace with the URL of the website containing images

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract the data you need from the HTML structure
    # For example, let's extract image URLs and their descriptions
    image_data_to_scrape = []
    for img_tag in soup.find_all('img'):
        src = img_tag['src']
        alt = img_tag.get('alt', '')
        image_data_to_scrape.append((src, alt))
    
    # Connect to a SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('image_data.db')  # Replace 'image_data.db' with your desired database name
    
    # Create a cursor object
    cursor = conn.cursor()
    
    # Define a table schema and create the table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scraped_images (
            id INTEGER PRIMARY KEY,
            src TEXT,
            description TEXT
        )
    ''')
    
    # Insert the scraped image data into the database
    cursor.executemany('INSERT INTO scraped_images (src, description) VALUES (?, ?)', image_data_to_scrape)
    
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()
    
    print('Image scraping and database insertion complete.')
else:
    print('Failed to retrieve data from the URL.')
