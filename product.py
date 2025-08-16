class Product:
    def __init__(self, id: int = None, name: str = '', price: float = 0.0, quantity: int = 0): # type: ignore
        self.id = id
        self.name = name
        self.price = price
        self.quantity = quantity

    def __repr__(self):
        return f"Product(id={self.id}, name='{self.name}', price={self.price}, quantity={self.quantity})"
