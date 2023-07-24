import os
import csv
import re
import requests
from bs4 import BeautifulSoup

# Function to split webpage into separate HTML files and create CSV
def split_webpage_to_files(webpage_url):
    # Send a request to get the webpage's content
    response = requests.get(webpage_url)
    if response.status_code != 200:
        print(f"Failed to fetch webpage. Status code: {response.status_code}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Create a directory to store the separate HTML files
    os.makedirs('section_files', exist_ok=True)

    # Create the CSV file
    with open('section_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Header', 'Date', 'Author'])

        # Find all section headers in the webpage
        section_headers = soup.find_all(['h2', 'h3', 'h4', 'h5', 'h6'])
        for header in section_headers:
            # Extract header text
            header_text = header.get_text(strip=True)

            # Use regular expressions to extract date and author information
            date_pattern = r'(?:\b\w+ \d{1,2},?\s?\'?\d{2,4}\b|\b\w+ \d{1,2}\b)'  # Match Month DD, YYYY or Month DD, YY or Month DD
            author_pattern = r'— (.+)$'  # Assuming the author name follows the last em dash

            date_match = re.search(date_pattern, header_text)
            author_match = re.search(author_pattern, header_text)

            date = date_match.group(0) if date_match else ''
            author = author_match.group(1) if author_match else ''

            # Create separate HTML file for each section
            section_filename = f'section_files/{header_text}.html'
            with open(section_filename, 'w', encoding='utf-8') as section_file:
                section_file.write(str(header) + '\n')

            # Append data to the CSV file
            csv_writer.writerow([header_text, date, author])

if __name__ == '__main__':
    webpage_url = 'https://bluemusemag.com/2020/03/13/coronavirus-notebook/'  # Replace with the URL of the webpage you want to process
    split_webpage_to_files(webpage_url)