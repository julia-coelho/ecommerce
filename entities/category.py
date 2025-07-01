#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from utils import Validator as v

#classe entidade category
class Category:
    def __init__(self, name: str, id: int|None = None) -> None:
        #validacao basica:
        if id is not None:
            v.validate_id(id)
        v.validate_name(name)

        #atribuicoes
        self.id = id
        self.name = name
    
    
    def __str__(self) -> str:
        return f"categoria {self.name}"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Category):
            if (self.id == None) or (other.id == None):
                return False
            return self.id == other.id            
        return False
    
    @staticmethod
    def validate_category(category: object) -> None:
        if not isinstance(category, Category):
            raise TypeError("category deve ser um objeto da classe Category")