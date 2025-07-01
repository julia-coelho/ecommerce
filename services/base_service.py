#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple
from abc import ABC, abstractmethod

from utils.validator import Validator as v
from dao.base_dao import BaseDAO

#classe service basica
class BaseService(ABC):
    def __init__(self, dao: BaseDAO) -> None:
        self.dao = dao


    def validate_existence_by_id(self, id: int) -> Tuple[bool, object]:
        """verifica se existe um registro com id 'id' na tabela associada ao dao"""

        v.validate_id(id)
        v.validate_id_size(id)

        found, obj = self.dao.find_by_id(id)

        if not found:
            return False, f"Registro de ID {id} da tabela {self.dao._get_table()}"
        return True, obj


    @abstractmethod
    def create_new(self, object_service) -> Tuple[bool, str]:
        """cria novo registro na tabela associada ao dao a partir de objeto de entidade (category, product, etc) validado"""
        pass

    
    @abstractmethod
    def update_by_id(self, id: int, object_service) -> Tuple[bool, str]:
        """atualiza registro existente na tabela associada ao dao com base no id 'id' fornecido e nos (novos) dados de 'object_service'"""
        pass


    def delete_by_id(self, id: int) -> Tuple[bool, str]:
        """remove um registro da tabela associada ao dao com base no id 'id' fornecido"""
        
        v.validate_id(id)
        v.validate_id_size(id)

        return self.dao.delete_by_id(id)
    
    
    @abstractmethod
    def list(self) -> Tuple[bool, list|str]:
        """lista registros da tabela associada ao dao conforme filtros especificos, se usar list(), lista todos os registros da tabela associada ao dao"""
        pass