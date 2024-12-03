# generate_music_prompt.py

import openai
import os
from extract_text import extract_text_from_epub  # Importer la fonction depuis le fichier extract_text.py

# Charger la clé API OpenAI à partir d'une variable d'environnement
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_music_context(book_text):
    """
    Fonction pour générer un contexte musical basé sur le texte du livre.
    Elle doit fournir un résumé concis du contexte, par exemple, des mots-clés liés à l'ambiance ou à la scène.

    Parameters:
    - book_text: Texte extrait du livre EPUB

    Returns:
    - str: Contexte musical généré, limité à 199 caractères
    """
    # Utiliser GPT pour analyser le texte et extraire un contexte musical
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Tu es un assistant qui génère des résumés de contexte pour une IA de musique."},
            {"role": "user", "content": f"Voici un extrait de livre : '{book_text[:20000]}'\nPeux-tu générer un contexte musical qui correspond à l'ambiance du texte ? Cela doit être une description succincte et précise, comme 'nature', 'calme', 'tristesse', etc."}
        ]
    )

    # Récupérer la réponse et la formater pour le contexte musical
    music_context = response['choices'][0]['message']['content']
    
    # Limiter la taille du contexte à 199 caractères
    music_context = music_context[:199]
    
    return music_context

# Exemple d'utilisation
if __name__ == "__main__":
    # Définir le chemin du fichier EPUB
    epub_file = '../Books/LE PETIT PRINCE.epub'
    
    # Extraire le texte du fichier EPUB
    book_text = extract_text_from_epub(epub_file)
    
    # Générer un contexte musical basé sur le texte extrait
    music_context = generate_music_context(book_text)
    
    # Afficher uniquement le contexte généré sans autres informations
    print(music_context)  # Cela affiche uniquement le contexte, sans texte du livre
    
    # Optionnel : sauvegarder le contexte dans un fichier
    with open('music_context.txt', 'w', encoding='utf-8') as f:
        f.write(music_context)

