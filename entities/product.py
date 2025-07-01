#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from utils import Validator as v
from utils import Normalizer as n
from entities import Category

#classe entidade product
class Product:
    def __init__(
            self, 
            name: str, 
            brand: str, 
            category: Category, 
            unit_price: float, 
            id: int|None = None,
            unit_discount: float = 0
    ) -> None:
        #validacao basica:
        if id is not None:
            v.validate_id(id)
        v.validate_name(name)
        v.validate_name(brand)
        Category.validate_category(category)
        v.validate_price(unit_price)
        v.validate_price(unit_discount)

        #verificacao precos
        if unit_discount > unit_price:
            raise ValueError(f"O desconto total aplicado ao produto {name}, marca {brand}, (R$ {unit_discount} é maior do que o valor do produto (R$ {unit_price})")

        #atribuicoes
        self.id = id
        self.name = name
        self.brand = brand
        self.category = category
        self.unit_price = unit_price
        self.unit_discount = unit_discount


    @property
    def final_unit_price(self) -> float:
        """preco final de um exemplar do product: unit_price - unit_discount"""
        return self.unit_price - self.unit_discount
    
    def __str__(self) -> str:
        return f"Produto {self.name}, marca {self.brand}, da {self.category} - {self.get_formatted_final_unit_price()} por unidade"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Product):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id            
        return False
    
    def get_formatted_unit_price(self) -> str:
        """retorna unit_price de product com apenas duas casas decimais e com R$"""
        return f"R$ {self.unit_price:.2f}"
    
    def get_formatted_unit_discount(self) -> str:
        """retorna unit_discount de product com apenas duas casas decimais e com R$"""
        return f"R$ {self.unit_discount:.2f}"
    
    def get_formatted_final_unit_price(self) -> str:
        """retorna final_unit_price (preco final de um exemplar do product) de product com apenas duas casas decimais e com R$"""
        return f"R$ {self.final_unit_price:.2f}"

    def matches_keyword(self, keyword: str) -> bool:
        """verifica se name, brand ou category de product batem com a palavra 'keyword' passada"""
        keyword_param = n.normalize(keyword)
        text = f"{self.name} {self.brand} {self.category.name}"
        text_param = n.normalize(text)
        return keyword_param in text_param

    def matches_category(self, category: Category) -> bool:
        """verifica se category de product bate com a categoria 'category' passada"""
        Category.validate_category(category)
        return self.category.id == category.id
    
    @staticmethod
    def validate_product(product: object) -> None:
        if not isinstance(product, Product):
            raise TypeError ("product deve ser um objeto da classe Product")