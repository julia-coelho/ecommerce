#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple

from services.base_service import BaseService
from utils.validator import Validator as v
from dao.product_dao import ProductDAO
from dao.category_dao import CategoryDAO
from entities.product import Product
from entities.category import Category

#classe service de product
class ProductService(BaseService):
    def __init__(self, dao: ProductDAO, category_dao: CategoryDAO) -> None:
        self.dao = dao
        self.category_dao = category_dao
    

    def create_new(self, object_service: Product) -> Tuple[bool, str]:

        #validacoes
        Product.validate_product(object_service)

        if object_service.id is not None:
            v.validate_id(object_service.id)
            v.validate_id_size(object_service.id)

        v.validate_name(object_service.name)
        v.validate_name_size(object_service.name)

        v.validate_name(object_service.brand)
        v.validate_name_size(object_service.brand)

        Category.validate_category(object_service.category)
        #verifica se a categoria associada existe
        if object_service.category.id is None:
            return False, f"ID de categoria de novo produto nao pode ser nulo"
        categoria_existe, _ = self.category_dao.find_by_id(object_service.category.id)
        if not categoria_existe:
            return False, f"Categoria de ID {object_service.category.id} não encontrada" 

        v.validate_price(object_service.unit_price)
        v.validate_price_size(object_service.unit_price)

        #chama metodo do dao
        return self.dao.create_new(object_service)
    

    def update_by_id(self, id: int, object_service: Product) -> Tuple[bool, str]:

        #validacoes
        v.validate_id(id)
        v.validate_id_size(id)
        found, _ = self.dao.find_by_id(id)

        if not found:
            return False, f"Produto de ID {id} não encontrado"

        Product.validate_product(object_service)

        v.validate_name(object_service.brand)
        v.validate_name_size(object_service.brand)

        Category.validate_category(object_service.category)
        #verifica se a categoria associada existe
        if object_service.category.id is None:
            return False, f"ID de nova categoria de produto não pode ser nulo"
        categoria_existe, _ = self.category_dao.find_by_id(object_service.category.id)
        if not categoria_existe:
            return False, f"Categoria de ID {object_service.category.id} não encontrada" 

        v.validate_price(object_service.unit_price)
        v.validate_price_size(object_service.unit_price)

        #chama metodo do dao
        return self.dao.update_by_id(id, object_service)
    

    #metodo para listar os produtos existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os produtos normalmente
    def list(
            self, 
            category_id=None, 
            brand=None, 
            min_unit_price=0, 
            max_unit_price=10**6, 
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> Tuple[bool, list|str]:

        #validacoes
        #category
        if category_id is not None:
            v.validate_id(category_id)
            v.validate_id_size(category_id)
            found_category, _ = self.category_dao.find_by_id(category_id)
            if not found_category:
                return False, f"Categoria de ID {category_id} não encontrada"
            
        #brand
        if brand is not None:
            v.validate_name(brand)
            v.validate_name_size(brand)
        
        #min and max prices
        if min_unit_price != 0:
            v.validate_price(min_unit_price)
            v.validate_price(min_unit_price)
        if max_unit_price != 10**6:
            v.validate_price(max_unit_price)
            v.validate_price_size(max_unit_price)


        #chama metodo do dao
        return True, self.dao.list(
            category_id=category_id, 
            brand=brand, 
            min_unit_price=min_unit_price, 
            max_unit_price=max_unit_price, 
            order_by_type=order_by_type, 
            asc_or_desc=asc_or_desc
        )



    #metodo para atualizar produto com base em nome passado
    def update_by_name(self, name: str, object_service: Product) -> Tuple[bool, str]:
        """atualiza produto na tabela com base no nome passado"""

        #validacoes
        v.validate_name(name)
        v.validate_name_size(name)

        found_object, object_objective = self.dao.find_by_name(name)

        if not found_object:
            return False, f"Produto {name} não encontrado"
        if object_objective is None:
            return False, f"Erro: Inconsistência, método product_dao.find_by_name afirmou que encontrou registro, mas passou none"
        if not object_objective.id:
            return False, f"Erro: Inconsistência, produto {name}, que existe no banco, não possui ID válida"

        Product.validate_product(object_service)

        v.validate_name(object_service.brand)
        v.validate_name_size(object_service.brand)

        Category.validate_category(object_service.category)
        #verifica se a categoria associada existe
        if object_service.category.id is None:
            return False, f"ID de nova categoria de produto não pode ser nulo"
        categoria_existe, _ = self.category_dao.find_by_id(object_service.category.id)
        if not categoria_existe:
            return False, f"Categoria de ID {object_service.category.id} não encontrada" 

        v.validate_price(object_service.unit_price)
        v.validate_price_size(object_service.unit_price)

        #chama metodo do dao
        return self.dao.update_by_id(object_objective.id, object_service)
    


    #/get_total_stock(batch_list: List<ProductBatch>, today: Date)