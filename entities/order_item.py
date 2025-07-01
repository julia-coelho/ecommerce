#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple

from utils import Validator as v
from entities import Product

#classe entidade orderitem
class OrderItem:
    def __init__(
            self, 
            product: Product, 
            order: "Order",
            id: int|None = None,
            quantity: int = 0,
            unit_price: float|None = None,
            unit_discount: float|None = None
    ) -> None:
        #validacao basica
        if id is not None:
            v.validate_id(id)
        Product.validate_product(product)
        from entities.order import Order
        Order.validate_order(order)
        v.validate_quantity(quantity)
        if unit_price is None:
            unit_price = product.unit_price
        v.validate_price(unit_price)
        if unit_discount is None:
            unit_discount = product.unit_discount
        v.validate_price(unit_discount)

        #verificacao precos
        if unit_discount > unit_price:
            raise ValueError(f"O desconto total aplicado ao produto {product.name}, marca {product.brand}, (R$ {unit_discount} é maior do que o valor do produto (R$ {unit_price})")

        #atribuicoes
        self.id = id
        self.product = product
        self.order = order
        self.quantity = quantity
        self.unit_price = unit_price
        self.unit_discount = unit_discount
        self.batches = []

    
    @property
    def total_price(self) -> float:
        """o preco de todos os exemplares no order_item"""
        total = self.final_unit_price * self.quantity
        return total
    
    @property
    def final_unit_price(self) -> float:
        """o preco final de um exemplar (unit_price - unit_discount) do orderitem"""
        return self.unit_price - self.unit_discount
    
    def __str__(self) -> str:
        return (
            f"{self.quantity} X {self.product.name} (marca {self.product.brand})"
            f"(a {self.get_formatted_final_unit_price()} cada) - "
            f"Total: {self.get_formatted_total_price()}"
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, OrderItem):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id
        return False
    
    def get_formatted_total_price(self) -> str:
        """retorna o total_price do orderitem com apenas duas casas decimais e com R$"""
        return f"R$ {self.total_price:.2f}"
    
    def get_formatted_final_unit_price(self) -> str:
        """retorna o preco final de um exemplar (unit_price - unit_discount) do orderitem com apenas duas casas decimais e com R$"""
        return f"R$ {self.final_unit_price:.2f}"
    
    def add_order_item_batch(self, batch: "OrderItemBatch") -> None:
        """adciona um orderitembatch no atributo batches: list[OrderItemBatch] do orderitem - deve ser usada exclusivamente para ordersitems que *nao* vieram do db"""
        from entities.order_item_batch import OrderItemBatch
        OrderItemBatch.validate_order_item_batch(batch)
        if batch.order_item.id != self.id:
            raise ValueError(f"Inconsistente: o item-pedido-lote de ID {batch.id} não se refere ao item de pedido de ID {self.id}, mas ao item de pedido de ID {batch.order_item.id}")
        #acrescenta a quantidade de batch a quantidade do orderitem
        self.quantity += batch.quantity
        #se ja houver algum orderitembatch daquele product_batch em orderitem, apenas aumenta a quantidade do orderitembatch ja existente
        for b in self.batches:
            if b.product_batch.id == batch.product_batch.id:
                b.quantity += batch.quantity
                return
        #se nao, acrescenta batch no atributo batches
        self.batches.append(batch)
        return

    def add_order_item_batch_from_db(self, batch: "OrderItemBatch") -> None:
        """adciona um orderitembatch no atributo batches: list[OrderItemBatch] do orderitem - deve ser usada exclusivamente para ordersitems que *vieram* do db"""
        from entities.order_item_batch import OrderItemBatch
        OrderItemBatch.validate_order_item_batch(batch)
        if batch.order_item.id != self.id:
            raise ValueError(f"Inconsistente: o item-pedido-lote de ID {batch.id} não se refere ao item de pedido de ID {self.id}, mas ao item de pedido de ID {batch.order_item.id}")
        #acrescenta batch a orderitem
        batches_quantity = batch.quantity
        for b in self.batches:
            batches_quantity += b.quantity
            if batch.product_batch.id == b.product_batch.id:
                raise ValueError(f"Inconsistente: banco com dois item_pedido_lote iguais")
        if batches_quantity > self.quantity:
            raise ValueError(f"Inconsistente: a soma da quantidade de exemplares de diferentes lotes ({batches_quantity}) do item é maior do que a quantidade total do item ({self.quantity})")
        self.batches.append(batch)

    def get_product_name_and_brand(self) -> Tuple[str, str]:
        return self.product.name, self.product.brand

    @staticmethod
    def validate_order_item(order_item: object) -> None:
        if not isinstance(order_item, OrderItem):
            raise TypeError("order_item deve ser um objeto da classe OrderItem")