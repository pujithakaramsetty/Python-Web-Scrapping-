import requests
from bs4 import BeautifulSoup
import csv

def get_part_of_speech(word):
    # Merriam-Webster Dictionary URL
    url = f'https://www.merriam-webster.com/dictionary/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Fetch the webpage
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        entry_section = soup.find(id="dictionary-entry-1")
        
        if entry_section:
            pos_tag = entry_section.find("a", class_="important-blue-link")
            
            if pos_tag:
                return pos_tag.get_text().strip()
        
        return "Part of speech not found."
    elif response.status_code == 404:
        return "Word not found (404)."
    return f"Error: {response.status_code}"

# Read words from the input file
input_file = 'Test.txt'  # Your input file containing words

# Open the output CSV file
output_file = 'output.csv'

with open(input_file, 'r', encoding='utf-8') as infile:
    words = infile.readlines()

# Open CSV to write results
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Part of Speech'])  # Writing header
    
    for word in words:
        word = word.strip()  # Remove any extra spaces or newlines
        part_of_speech = get_part_of_speech(word)  # Fetch part of speech
        writer.writerow([word, part_of_speech])  # Write to CSV

print(f"Results have been saved to {output_file}.")
