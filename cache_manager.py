from flask import Flask, request
import flask
import time
import json
import os
import plyvel
# Sample data in the cache
"""
cache_data {
    {
        {
            'identifier': 'BX80684I99900K;
            'amazon_data': ['Amazon', '$484.99', 'https://www.amazon.com/s?k=BX80684I99900K&i=electronics&rh=n%3A172282&qid=1563197272&ref=sr_hi_1'], 
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

db = None
app = Flask(__name__)

@app.route('/', methods=['PUT', 'GET', 'DELETE'])
def start():
    if request.method == "GET":
        """
        Sends back the requested retailer data for the specific
        item model given
        """
        
        try:
            item_model = request.args.get('item_model')
            stored_data = db.get(bytes(item_model, encoding='utf-8'))

            # Must use [2:-1] on the string because the beginning
            # of the string has 'b and the end has '
            # In order for it to be a valid dictionary, must remove them
            stored_data = json.loads(str(stored_data)[2:-1])
            return {'success': True, 'data': stored_data}, 200

        except Exception as e:
            print(str(e))
            return json.dumps({'success': False}), 404

    elif request.method == "PUT":
        """
        PUT request will have just the regular JSON response stored
        in the leveldb database
        """

        try:
            response = request.json

            # The key that will be stored in the database
            identifier = response['identifier']
            db.put(bytes(identifier, encoding='utf-8'), bytes(json.dumps(response), encoding='utf-8'))
            return json.dumps({'success': True}), 204
        
        except Exception as e:
            print(str(e))
            return json.dumps({'success': False, 'message': str(e)}), 500

    elif request.method == "DELETE":
        """
        Given an identifier, delete the resource from 
        the database
        """

        try: 
            identifier = request.json['identifier']
            db.delete(bytes(identifier, encoding='utf-8'))
            return json.dumps({'success': True}), 200
            
        except Exception as e:
            return json.dumps({'success': False, 'message': str(e)}), 500

if __name__ == "__main__":
    if not os.path.exists(r'./databases'):
        os.makedirs(r'./databases')

    db = plyvel.DB('databases/db', create_if_missing=True)
    app.run(host="localhost", port=5001, threaded=True)
