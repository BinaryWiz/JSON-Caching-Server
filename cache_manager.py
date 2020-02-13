from flask import Flask, request
import flask
import time
import json
import os
import plyvel
import requests

# Set up databases
if not os.path.exists(r'./databases'):
    os.makedirs(r'./databases')

request_db = plyvel.DB('databases/request_db', create_if_missing=True)
time_db = plyvel.DB('databases/time_db', create_if_missing=True)

app = Flask(__name__)


@app.route('/', methods=['PUT', 'GET', 'DELETE'])
def start():
    if request.method == "GET":
        """
        Sends back the requested retailer data for the specific
        item model given
        """
        
        try:
            identifier = request.args.get('identifier')
            stored_data = request_db.get(bytes(identifier, encoding='utf-8'))
            # If data was found, continue
            if (stored_data != None):
                # Must use [2:-1] on the string because the beginning
                # of the string has 'b and the end has '
                # In order for it to be a valid dictionary, must remove them
                
                stored_data = json.loads(str(stored_data)[2:-1])
                stored_data['success'] = True
                return stored_data, 200

            else:
                return json.dumps({'success': False}), 404

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
            response['success'] = True

            request_db.put(bytes(identifier, encoding='utf-8'), bytes(json.dumps(response), encoding='utf-8'))
            time_db.put(bytes(identifier, encoding='utf-8'), bytes([0]))
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
            print(identifier)
            request_db.delete(bytes(identifier, encoding='utf-8'))

            return json.dumps({'success': True}), 200
            
        except Exception as e:
            return json.dumps({'success': False, 'message': str(e)}), 500


@app.route('/check', methods=['GET'])
def check_database():
    if request.method == 'GET':
        try:
            for key, value in request_db:
                print(key, value, int.from_bytes(time_db.get(key), byteorder='big'))
            
            return json.dumps({'success': True}), 200

        except Exception as e:
            print(str(e))
            return json.dumps({'success': False}), 404

TIME_DELETIION = 30
TIME_MINUTES = 1

@app.route('/update', methods=['GET'])
def time_updater():
    """
    Updates how long each entry has been in the database.
    Deletes after the amount of minutes have passed as
    defined in TIME_DELETION
    """
    try:
        TIME_MINUTES = int(request.args.get('mins'))  
        for key, value in time_db:
            # Adds to the time_db via the amount of time defined in TIME_MINUTES
            time_db.put(key, bytes([int.from_bytes(value, byteorder='big') + 
                int.from_bytes([TIME_MINUTES], byteorder='big')])) 
            
            if value == bytes([TIME_DELETIION]):
                time_db.delete(key)
                requests.delete('http://localhost:5001/', json={'identifier': key.decode('utf-8')})
        
        return json.dumps({'success': True}), 204

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    app.run(host="localhost", port=5001, threaded=True)
