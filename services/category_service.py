#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple

from services.base_service import BaseService
from utils.validator import Validator as v
from dao.category_dao import CategoryDAO
from entities.category import Category

#classe service de product
class CategoryService(BaseService):
    def __init__(self, dao: CategoryDAO) -> None:
        self.dao = dao
    

    def create_new(self, object_service: Category) -> Tuple[bool, str]:

        #validacoes
        Category.validate_category(object_service)

        if object_service.id is not None:
            v.validate_id(object_service.id)
            v.validate_id_size(object_service.id)

        v.validate_name(object_service.name)
        v.validate_name_size(object_service.name)

        #chama metodo do dao
        return self.dao.create_new(object_service)
    

    def update_by_id(self, id: int, object_service: Category) -> Tuple[bool, str]:

        #validacoes
        v.validate_id(id)
        v.validate_id_size(id)

        Category.validate_category(object_service)

        found, _ = self.dao.find_by_id(id)
        if not found:
            return False, f"Categoria de ID {id} nao encontrada"

        #chama metodo do dao
        return self.dao.update_by_id(id, object_service)
    

    #metodo para listar os produtos existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os produtos normalmente
    def list(
            self, 
            min_product_amount=0, 
            max_product_amount=10**6, 
            no_products=False, 
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> Tuple[bool, list]:
        #validacoes
        #min and max products
        if min_product_amount != 0:
            v.validate_quantity(min_product_amount)
            v.validate_quantity_size(min_product_amount)
        if max_product_amount != 10**6:
            v.validate_quantity(max_product_amount)
            v.validate_quantity_size(max_product_amount)

        #chama metodo do dao
        return True, self.dao.list(
            min_product_amount=min_product_amount, 
            max_product_amount=max_product_amount, 
            no_products=no_products, 
            order_by_type=order_by_type, 
            asc_or_desc=asc_or_desc
        )