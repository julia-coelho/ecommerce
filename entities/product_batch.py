#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple

from utils import Validator as v
from entities import Product
from entities import Date

#classe entidade productbatch
class ProductBatch:
    def __init__(
            self, 
            product: Product, 
            batch_number: str, 
            manufacturing_date: Date, 
            quantity: int,
            id: int|None = None,
            due_date: Date|None = None
    ) -> None:
        #validacao basica
        if id is not None:
            v.validate_id(id)
        Product.validate_product(product)
        v.validate_alpha_numeric(batch_number)
        Date.validate_date(manufacturing_date)
        if due_date is not None:
            Date.validate_date(due_date)
        v.validate_quantity(quantity)


        #atribuicoes
        self.id = id
        self.product = product
        self.batch_number = batch_number
        self.manufacturing_date = manufacturing_date
        self.due_date = due_date
        self.quantity = quantity

        
    @property
    def unit_price(self) -> float:
        return self.product.unit_price
    
    @property
    def unit_discount(self) -> float:
        return self.product.unit_discount
    
    @property
    def final_unit_price(self) -> float:
        return self.product.final_unit_price

    def __str__(self) -> str:
        return (
            f"Lote de ID {self.id} no Estoque - {self.product}, Lote #{self.batch_number}, "
            f"Quantidade: {self.quantity}, "
            f"Preço Unitário: {self.get_formatted_final_price()}"
        )
    
    def __eq__(self, other: object) -> bool:
        if isinstance(other, ProductBatch):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id
        return False
    
    def get_product_id(self) -> int:
        return self.product.id
    
    def get_product_name_and_brand(self) -> Tuple[str, str]:
        return self.product.name, self.product.brand
    
    def get_formatted_final_price(self) -> str:
        """retorna o preco final do productbatch com apenas duas casas decimais e com R$"""
        return f"R$ {self.final_unit_price:.2f}"
    
    def days_until_expiration(self) -> int|None:
        """retorna quantidade de dias ate o productbatch expirar, se ele tiver uma due_date. se nao, retorna none"""
        if self.due_date is None:
            return None
        return (self.due_date.to_date() - Date.datetime_today()).days
    
    def is_expired(self) -> bool:
        """retorna true se a data de validade tiver passado, false se ela ainda nao passou"""
        if self.due_date is None:
            return False
        return self.due_date.to_date() < Date.datetime_today()
    
    @staticmethod
    def validate_product_batch(product_batch: object) -> None:
        if not isinstance(product_batch, ProductBatch):
            raise TypeError("product_batch deve ser um objeto da classe ProductBatch")