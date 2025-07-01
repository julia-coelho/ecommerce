#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from typing import Tuple
from abc import ABC, abstractmethod
import sqlite3

#classe dao básica
class BaseDAO(ABC):
    def __init__(self, conexao) -> None:
        self.conexao = conexao
 
    
    @abstractmethod
    def _get_table(self) -> str:
        """nome da tabela no banco"""
        pass


    @abstractmethod
    def _row_to_object(self, row) -> object: # o metodo vai retornar um object, que vai variar conforme qual DAO especifico (ex: CategoryDAO._row_to_object()) retorna um objeto da classe Category)
        """converte um registro da tabela em uma versão leve de um objeto, sem nenhum atributo-lista (ex: converte um registro de cliente em um Customer sem nenhuma Order em orders)"""
        pass


    @abstractmethod
    def _row_to_full_object(self, row) -> object: # o metodo vai retornar um object, que vai variar conforme qual DAO especifico (ex: CategoryDAO._row_to_object()) retorna um objeto da classe Category)
        """converte um registro da tabela em um objeto completo, com atributos-lista (ex: converte um registro de cliente em um Customer com todas suas Orders, cada Order com seus OrderItems e cada OrderItem com seus OrderItemBatchs)"""
        pass


    def find_by_id(self, id: int) -> Tuple[bool, object|None]: # o metodo vai retornar Tuple[bool, object], em que object vai variar conforme o DAO especifico (ex: CategoryDAO.find_by_id(id) retorna um object da classe Category)
        """busca registro de id 'id', verifica se existe no banco e, se existir, constroi versao (sem nenhum atributo-lista)"""
        cursor = self.conexao.cursor()
        cursor.execute(f"SELECT * FROM {self._get_table()} WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return True, self._row_to_object(row)
        return False, None
    

    def find_by_id_full_object(self, id: int) -> Tuple[bool, object|None]: # o metodo vai retornar Tuple[bool, object], em que object vai variar conforme o DAO especifico (ex: CategoryDAO.find_by_id(id) retorna um object da classe Category)
        """busca registro de id 'id', verifica se existe no banco e, se existir, constroi o objeto completo (com atributos-lista)"""
        cursor = self.conexao.cursor()
        cursor.execute(f"SELECT * FROM {self._get_table()} WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return True, self._row_to_full_object(row)
        return False, None


    @abstractmethod
    def create_new(self, object_entity) -> Tuple[bool, str]:
        """cria novo registro na tabela"""
        pass


    @abstractmethod
    def update_by_id(self, id, object_entity) -> Tuple[bool, str]:
        """atualiza registro de id 'id', usando os dados do objeto"""
        pass


    def delete_by_id(self, id: int) -> Tuple[bool, str]:
        """deleta registro de id 'id' """
        try:
            cursor = self.conexao.cursor()
            cursor.execute(f"DELETE FROM {self._get_table()} WHERE id = ?", (id,))
            self.conexao.commit()

            if cursor.rowcount == 0:
                return False, f"Erro: Registro da tabela {self._get_table()} de ID {id} não encontrado"
            return True, f"Registro de ID {id} da tabela {self._get_table()} deletado com sucesso"
        
        except sqlite3.IntegrityError as e:
            return False, f"Erro ao tentar deletar registro de ID {id} da tabela {self._get_table()}: {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"


    @abstractmethod
    def list(self) -> list[tuple]:
        """lista os registros da tabela conforme filtros - se chamar apenas list(), lista todos os registros da tabela"""
        pass


