# generate_music_prompt.py

import openai
import os
from extract_text import extract_text_from_epub

# Load OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_music_context(book_text):
    # Use GPT to analyze the text and extract a musical context
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an assistant generating context summaries for a music AI."},
            {"role": "user", "content": f"Here is a book excerpt: '{book_text[:20000]}'\nCan you generate a musical context that matches the mood of the text? Keep it concise and precise, like 'nature', 'calm', 'sadness', etc. 7 words is really the strict minimum."}
        ]
    )

    music_context = response['choices'][0]['message']['content']

    music_context = music_context[:199]
    
    return music_context

'''
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
'''
