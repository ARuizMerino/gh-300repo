from product import Product
from flask import Flask, request, render_template_string
from datetime import datetime

app = Flask(__name__)

class ProductManager:
    def __init__(self):
        self.products = []
        self.next_id = 1

    def add_product(self, name, price, quantity):
        product = Product(self.next_id, name, float(price), int(quantity))
        self.products.append(product)
        self.next_id += 1
        return f"Producto '{name}' agregado exitosamente."

    def list_products(self):
        return self.products

    def update_product(self, id, name=None, price=None, quantity=None):
        for product in self.products:
            if product.id == id:
                if name:
                    product.name = name
                if price:
                    product.price = float(price)
                if quantity:
                    product.quantity = int(quantity)
                return f"Producto ID {id} actualizado exitosamente."
        return f"Producto con ID {id} no encontrado."

    def delete_product(self, id):
        for i, product in enumerate(self.products):
            if product.id == id:
                del self.products[i]
                return f"Producto ID {id} eliminado exitosamente."
        return f"Producto con ID {id} no encontrado."

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
                    message = "Precio o cantidad inválidos."
            else:
                message = "Todos los campos son requeridos para agregar."
        elif action == 'update':
            id = request.form.get('id')
            name = request.form.get('update_name')
            price = request.form.get('update_price')
            quantity = request.form.get('update_quantity')
            if id:
                try:
                    message = manager.update_product(int(id), name or None, float(price) if price else None, int(quantity) if quantity else None)
                except ValueError:
                    message = "ID, precio o cantidad inválidos."
            else:
                message = "ID es requerido para actualizar."
        elif action == 'delete':
            id = request.form.get('delete_id')
            if id:
                try:
                    message = manager.delete_product(int(id))
                except ValueError:
                    message = "ID inválido."
            else:
                message = "ID es requerido para eliminar."
    
    products = manager.list_products()
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Sistema de Gestión de Productos</title>
</head>
<body>
    <h1>Sistema de Gestión de Productos</h1>
    <p>{{ message }}</p>
    
    <h2>Agregar Producto</h2>
    <form method="post">
        <input type="hidden" name="action" value="add">
        Nombre: <input type="text" name="name"><br>
        Precio: <input type="text" name="price"><br>
        Cantidad: <input type="text" name="quantity"><br>
        <input type="submit" value="Agregar">
    </form>
    
    <h2>Actualizar Producto</h2>
    <form method="post">
        <input type="hidden" name="action" value="update">
        ID: <input type="text" name="id"><br>
        Nombre: <input type="text" name="update_name"><br>
        Precio: <input type="text" name="update_price"><br>
        Cantidad: <input type="text" name="update_quantity"><br>
        <input type="submit" value="Actualizar">
    </form>
    
    <h2>Eliminar Producto</h2>
    <form method="post">
        <input type="hidden" name="action" value="delete">
        ID: <input type="text" name="delete_id"><br>
        <input type="submit" value="Eliminar">
    </form>
    
    <h2>Productos</h2>
    <table border="1">
        <tr><th>ID</th><th>Nombre</th><th>Precio</th><th>Cantidad</th><th>Fecha de Creación</th></tr>
        {% for product in products %}
        <tr>
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.price }}</td>
            <td>{{ product.quantity }}</td>
            <td>{{ product.created_at.strftime('%d/%m/%Y %H:%M:%S') }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
''', message=message, products=products)

def main():
    app.run(debug=True, port=5001)

if __name__ == "__main__":
    main()