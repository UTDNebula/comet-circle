import requests
import json

NEBULA_API_KEY = "dd1h55UQUb8x5nQIPW2iJ1ABaIDx9iv7"

headers = {"Authorization": NEBULA_API_KEY}

response = requests.get("https://api.utdnebula.com/v1/sections/search?days=Monday", headers=headers)
text = json.loads(response.text)