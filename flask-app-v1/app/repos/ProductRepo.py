from app.models.product import Product

class ProductRepo:

    def __init__(self, db):
        self.db = db

    def get_all(self):
        return Product.query.all()
    
    def get_by_id(self, product_id: int):
        return Product.query.get(product_id)
    
    def add(self, product):
        self.db.session.add(product)
        self.db.session.commit()
        return product
    
    def delete(self, product):
        self.db.session.delete(product)
        self.db.session.commit()
