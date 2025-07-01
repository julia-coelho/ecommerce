#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple

from utils import Validator as v

#classe entidade orderitembatch
class OrderItemBatch:
    def __init__(
            self,
            product_batch: "ProductBatch",
            order_item: "OrderItem", 
            quantity: int, 
            id: int|None = None
    ) -> None:
        #validacao basica
        if id is not None:
            v.validate_id(id)
        from entities.product_batch import ProductBatch
        ProductBatch.validate_product_batch(product_batch)
        from entities.order_item import OrderItem
        OrderItem.validate_order_item(order_item)
        v.validate_quantity(quantity)

        #verificacao se o product de product_batch eh o mesmo de order_item
        if product_batch.product.id != order_item.product.id:
            raise ValueError(f"Inconsistente: produto do lote {product_batch.product.name}, marca {product_batch.product.brand} não é o mesmo produto do item do pedido {order_item.product.name}, marca {order_item.product.brand}")

        #atribuicoes
        self.id = id
        self.product_batch = product_batch
        self.order_item = order_item
        self.quantity = quantity

    
    def __str__(self) -> str:
        name, brand = self.get_product_name_and_brand()
        return (
            f"{self.quantity} "
            f"do produto {name}, marca {brand}"
            f", lote #{self.product_batch.batch_number}"
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrderItemBatch):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id
        return False
    
    def is_from_expired_batch(self) -> bool:
        return self.product_batch.is_expired()
    
    def get_product_name_and_brand(self) -> Tuple[str, str]:
        return self.product_batch.product.name, self.product_batch.product.brand
    
    @staticmethod
    def validate_order_item_batch(order_item_batch) -> None:
        if not isinstance(order_item_batch, OrderItemBatch):
            raise TypeError("order_item_batch deve ser um objeto da classe OrderItemBatch")
    
