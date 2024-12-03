# extract_text.py

import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def extract_text_from_epub(epub_file):
    """
    Extrait le texte d'un fichier EPUB.

    Parameters:
    - epub_file : chemin vers le fichier EPUB à traiter

    Returns:
    - str : Le texte extrait du fichier EPUB
    """
    # Ouvrir le fichier EPUB
    book = epub.read_epub(epub_file)
    
    # Initialiser une variable pour stocker le texte extrait
    text = ''
    
    # Parcourir les éléments du livre (les chapitres et le contenu)
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Utiliser BeautifulSoup pour extraire le texte des fichiers HTML
            soup = BeautifulSoup(item.content, 'html.parser')
            text += soup.get_text()  # Ajouter le texte extrait à la variable `text`
    
    return text  # Ne rien afficher ici, juste retourner le texte

