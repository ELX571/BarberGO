import os
from dotenv import load_dotenv
from google import genai

load_dotenv('/home/ismoilow/Desktop/my project/BarberGo/.env')
api_key = os.getenv('GEMINI_API_KEY')

client = genai.Client(api_key=api_key)
for model in client.models.list():
    if 'generateContent' in model.supported_actions:
        print(model.name)
