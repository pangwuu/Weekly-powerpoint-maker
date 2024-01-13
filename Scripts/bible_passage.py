import requests
from bs4 import BeautifulSoup
import pyperclip
import re

class NoTextFoundException(Exception):
    def __init__(self, message="No text found in the file."):
        self.message = message
        super().__init__(self.message)

def remove_letters_in_brackets(text):
    # Use regular expression to match text within both round and square brackets (single or double character) and remove them
    if text is None:
        raise NoTextFoundException()
    cleaned_text = re.sub(r'[\[\(][A-Za-z]{1,2}[\]\)]', '', text)
    cleaned_text = re.sub(r'\(\w{2}\)', '', cleaned_text)
    return cleaned_text

def get_bible_verse(verse_reference):
    url = f"https://www.biblegateway.com/passage/?search={verse_reference}&version=NIV"
    
    try:
        response = requests.get(url)
    except:
        raise ConnectionError()
    
    print(response)
    

    soup = BeautifulSoup(response.content, 'html.parser')
    
    passage = soup.find("div", {"class": "passage-text"})
    if passage:
        verses = passage.find_all("span", {"class": "text"})
        verse_text = " ".join([verse.get_text() for verse in verses])
        return verse_text
    else:
        return None

def split_verse_into_parts(verse_text, words_per_part=175, sentences_per_part = 10):
    parts = []

    verse_sentences = verse_text.split('.')
    i = 0

    for i in range(len(verse_sentences)):
        try:
            if (verse_sentences[i][-1] != '"'):
                verse_sentences[i] = verse_sentences[i] + '.'
        except:
            pass
        i += 1
    
    current_part = []
    sentence_count = 0

    for sentence in verse_sentences:
        current_part.append(sentence)
        sentence_count += 1
    
        if len(current_part) >= sentences_per_part:
            part = " ".join(current_part)
            parts.append(part)
            current_part = []
            sentence_count = 0
    
    
    # for word in verse_words:
    #     current_part.append(word)
    #     word_count += 1
        
    #     if word_count >= words_per_part:
    #         part = " ".join(current_part)
    #         parts.append(part)
    #         current_part = []
    #         word_count = 0
    
    if current_part:
        part = " ".join(current_part)
        parts.append(part)
    
    
    return parts


def bible_passage():
    while True:
        verse_reference = input("Enter a Bible verse reference such as '2 Peter 1:5-11' (n to exit)\n")
        
        if verse_reference.lower().strip() == "n":
            return
        
        try:
            verse_text = remove_letters_in_brackets(get_bible_verse(verse_reference))
            break
        except NoTextFoundException:
            go_again = input("No text found. Would you like to try again? (Y for yes, any other key to exit)\n")
            if go_again.lower().strip() == "y":
                continue
            else:
                return
        except ConnectionError:
            go_again = input("Could not connect to the API. Check your internet connection. Would you like to try again? (Y for yes, any other key to exit)\n")
            if go_again.lower().strip() == "y":
                continue
            else:
                return


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
    
<<<<<<< Updated upstream
    return parts
=======
    return parts
>>>>>>> Stashed changes
