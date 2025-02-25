import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

# Suppress unwanted log messages
logging.getLogger('selenium.webdriver.remote.remote_connection').setLevel(logging.WARNING)
logging.getLogger('selenium.webdriver.chrome.webdriver').setLevel(logging.WARNING)
logging.getLogger('selenium.webdriver.chrome.service').setLevel(logging.WARNING)

def get_part_of_speech(word):
    # Collins Dictionary URL
    url = f"https://www.collinsdictionary.com/dictionary/english/{word}"
    
    # Set up Chrome options to suppress logs
    options = Options()
    options.headless = True  # Run the browser in headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])  # Remove "DevTools listening" and other logs
    
    # Start the Chrome WebDriver
    service = Service(ChromeDriverManager().install())  # Use webdriver_manager to install and manage chromedriver
    driver = webdriver.Chrome(service=service, options=options)
    
    driver.get(url)

    # Wait for the content to load. Wait until we can find the part of speech element
    try:
        # Adjust this timeout as needed based on how long the page takes to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "content.definitions.ced"))
        )
        
        content_div = driver.find_element(By.CLASS_NAME, "content.definitions.ced")
        hom_div = content_div.find_element(By.CLASS_NAME, "hom")
        pos_element = hom_div.find_element(By.CLASS_NAME, "pos")
        
        part_of_speech = pos_element.text.strip()
    except Exception:
        part_of_speech = "Part of speech not found."
    
    driver.quit()
    
    return part_of_speech

def read_words_from_file(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read().splitlines()  # Reads each line as a separate word

def write_results_to_csv(results, output_filename="output_collins.csv"):
    with open(output_filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ['Word', 'Part of Speech']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)

# Main process
input_file = "test.txt"  # File containing the words
words = read_words_from_file(input_file)

results = []
for word in words:
    print(f"Processing: {word}")  # Show which word is being processed
    part_of_speech = get_part_of_speech(word)
    results.append({'Word': word, 'Part of Speech': part_of_speech})

write_results_to_csv(results)

print("Results saved to output_collins.csv.")
