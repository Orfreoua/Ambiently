# generate_music_prompt.py

import openai
import os
from extract_text import extract_text_from_epub

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_music_context(book_text):
    # Format the prompt to ask for emotional and musical context at different parts of the text
    prompt = f"""
    You are an assistant specializing in analyzing emotions and narrative moods in a text. I will provide you with an excerpt. Your task is to:

    1. Identify the dominant emotions or moods at the beginning, middle, and end of the text.
    2. Briefly describe how these emotions evolve.
    3. Provide a concise and evocative description of the musical atmospheres corresponding to these emotions. Limit yourself to 7 words maximum per musical atmosphere.

    Excerpt: "{book_text[:2000]}"  # Take the first 2000 characters of the excerpt

    Respond in the following format: 
    - Beginning: [dominant emotion], [musical atmosphere]
    - Middle: [dominant emotion], [musical atmosphere]
    - End: [dominant emotion], [musical atmosphere]

    If important transitions or nuances appear, add them briefly.
    """

    # Call OpenAI API to generate a response
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant helping to analyze texts and generate musical contexts."},
            {"role": "user", "content": prompt}
        ]
    )

    # Extract the music context from the response
    music_context = response['choices'][0]['message']['content']

    # Ensure the context is concise and doesn't exceed 200 characters
    music_context = music_context[:200]
    
    return music_context

# Example usage
if __name__ == "__main__":

    epub_file = '../Books/LE PETIT PRINCE.epub'

    # Extract text from the EPUB file
    book_text = extract_text_from_epub(epub_file)
    
    # Generate a musical context based on the extracted text
    music_context = generate_music_context(book_text)

    print(music_context)  # This only displays the context, without the book text
    
    # Optional: save the context to a file
    with open('music_context.txt', 'w', encoding='utf-8') as f:
        f.write(music_context)

