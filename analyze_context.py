import openai
import os

# Charger la clé API OpenAI à partir d'une variable d'environnement (plus sécurisé)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Exemple de requête GPT avec la méthode correcte
response = openai.ChatCompletion.create(
    model="gpt-4",  # Utilisez "gpt-3.5-turbo" si vous utilisez ce modèle
    messages=[
        {"role": "system", "content": "Tu es un assistant utile."},
        {"role": "user", "content": "Comment puis-je utiliser l'API OpenAI GPT avec Python ?"}
    ]
)

# Afficher la réponse générée
print("Réponse de GPT :")
print(response['choices'][0]['message']['content'])
