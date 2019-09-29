import requests
import json

while True:
    user_input = input("Would you like to GET PUT or DELETE? ")

    if user_input.upper() == "GET":
        r = requests.get(url = "http://localhost:5001?item_model=BX80684I99900") 
        print(r.json())
        
    elif user_input.upper() == "PUT":
        data = requests.get("http://localhost:5000/api/query?retailer=Newegg&price=525&item_model=BX80684I99900&return_type=json")
        load = data.json()
        print(load)
        r = requests.put(url = "http://localhost:5001/", json = load)
        
    elif user_input.upper() == "DELETE":
        data = requests.delete("http://localhost:5001/", json={'identifier': 'BX80684I99900'})
        response = data.json()
        print(response)
