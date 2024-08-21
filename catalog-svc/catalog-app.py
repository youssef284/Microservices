import json
from flask import Flask, request, jsonify, send_from_directory
import redis
import os

app = Flask(__name__)

# Connect to Redis (assuming Redis is running in a separate container)
r = redis.Redis(host='catalog-db', port=6379)

# Directory where images will be stored
IMAGE_DIR = '/root/app/images/'

# Ensure the image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

@app.route('/get-catalog', methods=['GET'])
def get_catalog():
    """Return the full image catalog."""
    data = r.hgetall("catalog")
    decoded_data = {}
    for key, value in data.items():
        decoded_key = key.decode('utf-8')
        decoded_value = json.loads(value.decode('utf-8'))
        decoded_data[decoded_key] = decoded_value
    return jsonify(decoded_data)

@app.route('/get-image/<image_id>', methods=['GET'])
def get_image(image_id):
    """Return details of a specific image."""
    image_data = r.hget("catalog", image_id)
    if image_data:
        image_data = json.loads(image_data.decode('utf-8'))
        return jsonify(image_data)
    else:
        return jsonify({"error": "Image not found"}), 404

@app.route('/get-images-by-tag/<tag>', methods=['GET'])
def get_images_by_tag(tag):
    """Return images that match a specific tag."""
    data = r.hgetall("catalog")
    filtered_data = {}
    for key, value in data.items():
        decoded_value = json.loads(value.decode('utf-8'))
        if tag in decoded_value.get('tags', []):
            filtered_data[key.decode('utf-8')] = decoded_value
    return jsonify(filtered_data)

@app.route('/images/<filename>')
def serve_image(filename):
    """Serve the image file from the images directory."""
    return send_from_directory(IMAGE_DIR, filename)
