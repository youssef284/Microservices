from flask import Flask, render_template
import requests

app = Flask(__name__)

# Route to display data from catalog service
@app.route('/catalog', methods=['GET'])
def get_catalog():
    """
    Retrieve the catalog and display it on a web page
    """
    try:
        # Fetch catalog data from the catalog service
        response = requests.get('http://catalog:5000/get-catalog', timeout=5)
        response.raise_for_status()  # Raise an error for bad HTTP status codes
        catalog_data = response.json()
        
        # Pass the catalog data to the template
        return render_template('shop-front-html.j2', catalog=catalog_data)
    except requests.RequestException as e:
        return f"An error occurred: {e}", 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
