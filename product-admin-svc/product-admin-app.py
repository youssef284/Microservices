from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Route to display the add-product page
@app.route('/add-product-page')
def add_product_page():
    """
    Return the add-product page
    """
    return render_template('add-product.html.j2')

# Route to add a new product to the catalog
@app.route('/add-product', methods=['POST'])
def add_product():
    """
    Add the new product to the catalog
    """
    product = {
        "make": request.form['make'],
        "model": request.form['model'],
        "price": request.form['price']
    }
    requests.post('http://catalog:5000/add-product', json=product, timeout=5)
    return "success"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
