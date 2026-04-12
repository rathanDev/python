from app.dto.product_dto import ProductDto
from app.models.product import Product

class ProductMapper:

    @staticmethod
    def to_dto(product: Product) -> ProductDto:
        return ProductDto(id=product.id, name=product.name, price=product.price)
    
    