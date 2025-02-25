import requests
from bs4 import BeautifulSoup
import csv

def get_part_of_speech_oxford(word):
    # Oxford Dictionary URL
    url = f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}'
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Fetch the webpage
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Try to find the part of speech using the current structure
        entry_section = soup.find('span', {'class': 'pos'})
        
        if entry_section:
            # Extract the part of speech (e.g., noun, verb)
            return entry_section.get_text().strip()
        
        return "Part of speech not found."
    
    elif response.status_code == 404:
        return "Word not found (404)."
    
    return f"Error: {response.status_code}"

# Read words from the input file
input_file = 'Test.txt'  # Your input file containing words

# Open the output CSV file
output_file = 'output_oxford.csv'

with open(input_file, 'r', encoding='utf-8') as infile:
    words = infile.readlines()

# Open CSV to write results
with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Word', 'Part of Speech'])  # Writing header
    
    for word in words:
        word = word.strip()  # Remove any extra spaces or newlines
        part_of_speech = get_part_of_speech_oxford(word)  # Fetch part of speech
        writer.writerow([word, part_of_speech])  # Write to CSV

print(f"Results have been saved to {output_file}.")
