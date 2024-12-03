import requests
import json
import dotenv
import os

# Load environment variables
dotenv.load_dotenv()

# Replace with your actual API key
API_KEY = os.getenv('GEMINI_API_KEY')

# Define the endpoint and headers
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=" + API_KEY
headers = {
    'Content-Type': 'application/json'
}

# Define the prompt and other parameters
data = {
    'contents': [
        {
            'parts': [
                {
                    'text': "Hello, how are you?"
                }
            ]
        }
    ]
}

# Send the request
response = requests.post(url, headers=headers, data=json.dumps(data))

# Print the response
if response.status_code == 200:
    print(response.json())
else:
    print(f'Error: {response.status_code}')
    print(response.text)
