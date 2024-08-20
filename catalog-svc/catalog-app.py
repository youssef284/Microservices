# flask app for product catalog
import json
from flask import Flask, request, jsonify
import redis 

app = Flask(__name__)


r = redis.Redis(host='catalog-db', port=6379)


catalog = {'catalog': {
    "Apple-iPhone6S": {"make": "Apple", "model": "iPhone 6s", "price": 699.99},
    "Apple-iPhone6SPlus": {"make": "Apple", "model": "iPhone 6s Plus", "price": 799.99},
    "Apple-iPhone7": {"make": "Apple", "model": "iPhone 7", "price": 749.99},
    "Apple-iPhone7Plus": {"make": "Apple", "model": "iPhone 7 Plus", "price": 869.99}
}}

# route get-catalog, returns json
@app.route('/get-catalog', methods=['GET'])
def get_catalog():
    # Get all keys and values from Redis
    data = r.hgetall("catalog")
    
    # Decode byte keys and values to strings
    decoded_data = {}
    for key, value in data.items():
        decoded_key = key.decode('utf-8')
        decoded_value = value.decode('utf-8')
        # Optionally, if the value is a JSON string, convert it back to a Python dict
        try:
            decoded_value = json.loads(decoded_value)
        except json.JSONDecodeError:
            # If the value is not a JSON string, keep it as is
            pass
        decoded_data[decoded_key] = decoded_value
    
    # Return the data as a JSON response
    return jsonify(decoded_data)

# add the new product to catalog (POST)
@app.route('/add-product', methods=['POST'])
def add_product():
    product = {
        "model": request.json['model'],
        "make": request.json['make'],
        "price": request.json['price']
    }
    
    # create key and value keys for make and product to string first
    key = f"catalog:{product['make']}:{product['model']}"
    
    # store the 'product' in redis. Convert json to string
    r.hset("catalog", key, json.dumps(product))
    
    return {'status': "ok"}



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
