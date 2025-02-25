import requests
from bs4 import BeautifulSoup

def get_part_of_speech(word):
    # Cambridge Dictionary URL
    cambridge_url = f"https://dictionary.cambridge.org/dictionary/english/{word}"
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Fetch from Cambridge Dictionary
    response = requests.get(cambridge_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        part_of_speech = soup.find('span', class_='pos')
        if part_of_speech:
            return part_of_speech.get_text().strip()
    
    # If not found, return None
    return None

def process_words_from_file(filename):
    with open(filename, 'r') as file:
        words = file.readlines()
    words = [word.strip() for word in words]
    
    for word in words:
        cambridge_pos = get_part_of_speech(word)
        if cambridge_pos:
            print(f"{word}:{cambridge_pos}")
        else:
            print(f"{word}:Not found")

filename = "test.txt"  # Your file name
process_words_from_file(filename)
