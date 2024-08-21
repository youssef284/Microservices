from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Route to display the catalog of images
@app.route('/catalog', methods=['GET'])
def get_catalog():
    """Retrieve the image catalog and display it on a web page."""
    try:
        # Fetch catalog data from the catalog service
        response = requests.get('http://catalog:5000/get-catalog', timeout=5)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        catalog_data = response.json()
        
        # Pass the catalog data to the template
        return render_template('catalog.html.j2', catalog=catalog_data)
    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

# Route to search images by tag
@app.route('/search', methods=['GET'])
def search_by_tag():
    """Search images by tag."""
    tag = request.args.get('tag')
    try:
        # Fetch filtered images by tag from the catalog service
        response = requests.get(f'http://catalog:5000/get-images-by-tag/{tag}', timeout=5)
        response.raise_for_status()
        filtered_data = response.json()
        
        # Pass the filtered data to the template
        return render_template('catalog.html.j2', catalog=filtered_data)
    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

# Route to display image details
@app.route('/image/<image_id>', methods=['GET'])
def image_details(image_id):
    """Display detailed information about a specific image."""
    try:
        # Fetch image details from the catalog service
        response = requests.get(f'http://catalog:5000/get-image/{image_id}', timeout=5)
        response.raise_for_status()
        image_data = response.json()
        
        # Pass the image data to the template
        return render_template('image-details.html.j2', image=image_data)
    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
