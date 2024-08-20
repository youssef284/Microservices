from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# Directory to store uploaded images
IMAGE_DIR = 'uploaded_images/'

# Ensure the image directory exists
os.makedirs(IMAGE_DIR, exist_ok=True)

# Route to display the add-image page
@app.route('/add-image-page')
def add_image_page():
    """Return the add-image page."""
    return render_template('add-image.html.j2')

# Route to add a new image to the catalog
@app.route('/add-image', methods=['POST'])
def add_image():
    """Add the new image to the catalog."""
    image_file = request.files['image']
    title = request.form['title']
    description = request.form['description']
    tags = request.form['tags'].split(',')

    # Save the image file to the designated directory
    image_path = os.path.join(IMAGE_DIR, image_file.filename)
    image_file.save(image_path)

    # Prepare the image metadata
    image_metadata = {
        "title": title,
        "description": description,
        "tags": tags,
        "image_path": image_path
    }

    # Send the metadata to the catalog service
    requests.post('http://catalog:5000/add-image', json=image_metadata, timeout=5)

    return redirect(url_for('add_image_page'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
