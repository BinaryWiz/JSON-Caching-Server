import requests
import json

data = requests.get("http://timeless-apps.com/api/query?retailer=Newegg&price=525&item_model=BX80684I99900K&return_type=json")
load = data.json()
load["item_model"] = "BX80684I99900K"
r = requests.post(url = "http://localhost:5000/", json = load) 
