from flask import Flask, request
import flask
import threading
import time
import json 

# Sample data in the cache
"""
cache_data {
    {
        item_model: ITEM MODEL,
        data: {'amazon_data': 
                ['Amazon', '$484.99', 'https://www.amazon.com/s?k=BX80684I99900K&i=electronics&rh=n%3A172282&qid=1563197272&ref=sr_hi_1'], 
                'bestbuy_data': [], 
                'newegg_data': ['Newegg', '525', '#'], 
                'walmart_data': ['Walmart', '$474.99', 'https://www.walmart.com/ip/Processor-Series-Lake-Coffee-Intel-UHD-630-16-Thread-Turbo-300-5-0-Core-BX80684I99900K-LGA-i9-9900K-1151-Graphics-8-Core-Desktop-GHz-3-6-95W/701836320'], 
                'bandh_data': ['B&H', '$484.99', 'https://www.bhphotovideo.com/c/product/1435917-REG/intel_bx80684i99900k_core_i9_9900k_3_6_ghz.html'],
                'ebay_data': ['Ebay', '$549.00', 'https://www.ebay.com/sch/i.html?_odkw=BX80684I99900K&_osacat=0&_from=R40&_trksid=p2045573.m570.l1313.TR1.TRC0.A0.H0.TRS1&_nkw=BX80684I99900K&_sacat=0'], 
                'tigerdirect_data': ['Tiger Direct', '$565.99', 'http://www.tigerdirect.com/applications/SearchTools/item-details.asp?EdpNo=5956417&CatId=12405'], 
                'microcenter_data': ['Microcenter', '$449.99', 'https://www.microcenter.com/product/512483/core-i9-9900k-coffee-lake-36-ghz-lga-1151-boxed-processor'], 
                'jet_data': ['Jet', 'Could Not Find Price', 'None'], 
                'outletpc_data': ['OutletPC', '$358.90', 'https://www.outletpc.com/km3530.html'], 
                'superbiiz_data': ['SuperBiiz', '', 'None']
            }
    }
}
"""

app = Flask(__name__)

@app.route('/', methods=['PUT', 'GET', 'POST'])
def start():
    if request.method == "GET":
        item_model = request.args.get("item_model")
        with open("Cache/cache1.json", "r") as cache:
            cache = json.load(cache)
            for entry in cache["cache_data"]:
                if (entry.item_model_number) == item_model:
                    return entry.data

    elif request.method == "POST":
        with open('Cache/cache1.json', 'a+') as f:
            if not f.read(1):
                json.dump({"cache_data": []}, f)

        with open('Cache/cache1.json') as f:
            data = request.data
            

        return str({"hi": "HI"})

    elif request.method == "PUT":
        data = request.data
        with open("Cache/cache1.json", "a+") as cache:
            cache = json.load(cache)
            for entry in cache["cache_data"]:
                if (entry.item_model_number) == data.item_model:
                    entry.data = data.data

if __name__ == "__main__":
    app.run(host="localhost", debug = True)