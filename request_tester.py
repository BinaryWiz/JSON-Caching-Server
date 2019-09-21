import requests
import json

user_input = input("Would you like to GET PUT or POST? ")

if user_input == "GET":
    r = requests.get(url = "http://localhost:5001?item_model=BX80684I99900K",) 
    #print(r.json())

elif user_input == "POST":
    data = requests.get("http://timeless-apps.com/api/query?retailer=Newegg&price=525&item_model=BX80684I99900K&return_type=json")
    load = data.json()
    r = requests.post(url = "http://localhost:5001/", json = load) 
    
elif user_input == "PUT":
    data = requests.get("http://timeless-apps.com/api/query?retailer=Newegg&price=525&item_model=BX80684I99900K&return_type=json")
    load = data.json()
    print(load)
    load["amazon_data"] = ["Amazon", "$500", "X"]
    r = requests.put(url = "http://localhost:5001/", json = load) 
    