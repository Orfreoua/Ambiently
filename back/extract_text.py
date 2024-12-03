# extract_text.py

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_epub(epub_file):
    # Open the EPUB file
    book = epub.read_epub(epub_file)
    
    # Initialize a variable to store the extracted text
    text = ''
    
    # Iterate through the items in the book (chapters and content)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Use BeautifulSoup to extract text from HTML files
            soup = BeautifulSoup(item.content, 'html.parser')
            text += soup.get_text()
    
    return text
