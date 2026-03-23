from product import Product
from flask import Flask, request, render_template_string

app = Flask(__name__)

class ProductManager:
    def __init__(self):
        self.products = []
        self.next_id = 1

    def add_product(self, name, price, quantity):
        product = Product(self.next_id, name, float(price), int(quantity))
        self.products.append(product)
        self.next_id += 1
        return f"Product '{name}' added successfully."

    def list_products(self):
        if not self.products:
            return "No products available."
        return "\n".join(str(product) for product in self.products)

    def update_product(self, id, name=None, price=None, quantity=None):
        for product in self.products:
            if product.id == id:
                if name:
                    product.name = name
                if price:
                    product.price = float(price)
                if quantity:
                    product.quantity = int(quantity)
                return f"Product ID {id} updated successfully."
        return f"Product with ID {id} not found."

    def delete_product(self, id):
        for i, product in enumerate(self.products):
            if product.id == id:
                del self.products[i]
                return f"Product ID {id} deleted successfully."
        return f"Product with ID {id} not found."

manager = ProductManager()

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            name = request.form.get('name')
            price = request.form.get('price')
            quantity = request.form.get('quantity')
            if name and price and quantity:
                try:
                    message = manager.add_product(name, float(price), int(quantity))
                except ValueError:
                    message = "Invalid price or quantity."
            else:
                message = "All fields are required for adding."
        elif action == 'update':
            id = request.form.get('id')
            name = request.form.get('update_name')
            price = request.form.get('update_price')
            quantity = request.form.get('update_quantity')
            if id:
                try:
                    message = manager.update_product(int(id), name or None, float(price) if price else None, int(quantity) if quantity else None)
                except ValueError:
                    message = "Invalid ID, price, or quantity."
            else:
                message = "ID is required for updating."
        elif action == 'delete':
            id = request.form.get('delete_id')
            if id:
                try:
                    message = manager.delete_product(int(id))
                except ValueError:
                    message = "Invalid ID."
            else:
                message = "ID is required for deleting."
    
    products = manager.list_products()
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Product Management System</title>
</head>
<body>
    <h1>Product Management System</h1>
    <p>{{ message }}</p>
    
    <h2>Add Product</h2>
    <form method="post">
        <input type="hidden" name="action" value="add">
        Name: <input type="text" name="name"><br>
        Price: <input type="text" name="price"><br>
        Quantity: <input type="text" name="quantity"><br>
        <input type="submit" value="Add">
    </form>
    
    <h2>Update Product</h2>
    <form method="post">
        <input type="hidden" name="action" value="update">
        ID: <input type="text" name="id"><br>
        Name: <input type="text" name="update_name"><br>
        Price: <input type="text" name="update_price"><br>
        Quantity: <input type="text" name="update_quantity"><br>
        <input type="submit" value="Update">
    </form>
    
    <h2>Delete Product</h2>
    <form method="post">
        <input type="hidden" name="action" value="delete">
        ID: <input type="text" name="delete_id"><br>
        <input type="submit" value="Delete">
    </form>
    
    <h2>Products</h2>
    <pre>{{ products }}</pre>
</body>
</html>
''', message=message, products=products)

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()