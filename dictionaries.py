import requests
from bs4 import BeautifulSoup
import csv

# Define the headers for requests
headers = {'User-Agent': 'Mozilla/5.0'}

# Function to fetch part of speech from Oxford Dictionary
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

# Function to fetch part of speech from Cambridge Dictionary
def get_part_of_speech_cambridge(word):
    cambridge_url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    
    # Fetch from Cambridge Dictionary
    response = requests.get(cambridge_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        part_of_speech = soup.find('span', class_='pos')

        if part_of_speech:
            return part_of_speech.get_text().strip()
        
        return "Part of speech not found."
    elif response.status_code == 404:
        return "Word not found (404)."
    return f"Error: {response.status_code}"

# Function to fetch part of speech from Merriam-Webster Dictionary
def get_part_of_speech_merriam(word):
    mw_url = f'https://www.merriam-webster.com/dictionary/{word}'
    
    # Fetch the webpage
    response = requests.get(mw_url, headers=headers)
    
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

# Main function to process words and fetch parts of speech
def process_words_from_file(input_filename, output_filename):
    # Read words from input file
    with open(input_filename, 'r', encoding='utf-8') as infile:
        words = infile.readlines()

    # Prepare a dictionary to store words and their parts of speech from both dictionaries
    word_pos_dict = {}

    # Process each word and get the part of speech
    for word in words:
        word = word.strip()  # Clean up any extra spaces or newlines
        # Try fetching from Oxford
        oxford_pos= get_part_of_speech_oxford(word)

        # Try fetching from Cambridge 
        cambridge_pos = get_part_of_speech_cambridge(word)
        
        # Then fetch from Merriam-Webster
        merriam_pos = get_part_of_speech_merriam(word)

        # Store results in dictionary
        word_pos_dict[word] = (oxford_pos, cambridge_pos, merriam_pos)

    # Write results to CSV
    with open(output_filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Word','Part of Speech (Oxford)', 'Part of Speech (Cambridge)', 'Part of Speech (Merriam-Webster)'])  # Writing header
        
        for word, (oxford_pos, cambridge_pos, merriam_pos) in word_pos_dict.items():
            writer.writerow([word,oxford_pos, cambridge_pos, merriam_pos])  # Write word and parts of speech

    print(f"Results have been saved to {output_filename}.")

# Set filenames for input and output
input_file = 'Test.txt'  # Your input file containing words
output_file = 'output.csv'  # Output CSV file for results

# Call the main function to process the words
process_words_from_file(input_file, output_file)
