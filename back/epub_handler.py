# epub_handler.py
import os
from extract_text import extract_text_from_epub
from generate_music_prompt import generate_music_context

def process_epub(epub_file_path):
    """
    Function to process the uploaded EPUB file:
    1. Extract text from the EPUB.
    2. Generate a music context based on the text.
    """
    if not os.path.exists(epub_file_path):
        return None, "File not found"

    book_text = extract_text_from_epub(epub_file_path)

    music_context = generate_music_context(book_text)
    
    return music_context, None 
