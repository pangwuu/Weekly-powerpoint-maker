import requests
from bs4 import BeautifulSoup
import pyperclip
import re

def remove_letters_in_brackets(text):
    # Use regular expression to match text within both round and square brackets (single or double character) and remove them
    cleaned_text = re.sub(r'[\[\(][A-Za-z]{1,2}[\]\)]', '', text)
    return cleaned_text

def get_bible_verse(verse_reference):
    url = f"https://www.biblegateway.com/passage/?search={verse_reference}&version=NIV"
    
    try:
        response = requests.get(url)
    except ConnectionError:
        return "Could not connect to the api. Please check your internet connection"
    

    soup = BeautifulSoup(response.content, 'html.parser')
    
    passage = soup.find("div", {"class": "passage-text"})
    if passage:
        verses = passage.find_all("span", {"class": "text"})
        verse_text = " ".join([verse.get_text() for verse in verses])
        return verse_text
    else:
        return None

def split_verse_into_parts(verse_text, words_per_part=175):
    parts = []
    
    verse_words = verse_text.split()  # Split the text into words
    current_part = []
    word_count = 0
    
    for word in verse_words:
        current_part.append(word)
        word_count += 1
        
        if word_count >= words_per_part:
            part = " ".join(current_part)
            parts.append(part)
            current_part = []
            word_count = 0
    
    if current_part:
        part = " ".join(current_part)
        parts.append(part)
    
    return parts


def bible_passage():
    verse_reference = input("Enter a Bible verse reference (e.g., '2 Peter 1:5-11'): ")
    
    verse_text = remove_letters_in_brackets(get_bible_verse(verse_reference))
    if verse_text:
        # Split the verse into 5-verse long parts
        parts = split_verse_into_parts(verse_text)
        
        for i, part in enumerate(parts):
            pyperclip.copy(part)
            print(f"Part {i + 1} - Bible verse copied to clipboard:")
            print(part)
            if i < len(parts) - 1:
                input("Press Enter to copy the next part...")
    else:
        print("Verse not found or error occurred.")

def split_bible_text(bible_text, verses_per_part=5):
    verses = bible_text.split('\n')
    parts = [verses[i:i + verses_per_part] for i in range(0, len(verses), verses_per_part)]
    
    return parts