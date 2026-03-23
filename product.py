from datetime import datetime

class Product:
    def __init__(self, id, name, price, quantity, created_at=None):
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity
        self.created_at = created_at or datetime.now()

    def __str__(self):
        fecha_formateada = self.created_at.strftime("%d/%m/%Y %H:%M:%S") if isinstance(self.created_at, datetime) else self.created_at
        return f"ID: {self.id}, Nombre: {self.name}, Precio: {self.price}, Cantidad: {self.quantity}, Creado: {fecha_formateada}"