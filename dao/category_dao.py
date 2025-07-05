#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Any

from dao.base_dao import BaseDAO
from entities import Category
from utils import Normalizer as n

#classe dao de category
class CategoryDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "categorias"
    

    def _row_to_object(self, row) -> Category:
        id, name = row
        return Category(name=name, id=id)
    
    def _row_to_full_object(self, row) -> Category:
        return self._row_to_object(row)
    

    def create_new(self, object_entity: Category) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            cursor.execute("INSERT INTO categorias (nome) VALUES(?)",
                           (object_entity.name,))
            self.conexao.commit()
            return True, f"Nova categoria '{object_entity.name}' foi criada com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: A categoria '{object_entity.name}' já existe.  Verifique se está tentando duplicar uma categoria já registrada"
            else:
                return False, f"Erro ao criar nova categoria '{object_entity.name}': {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id, object_entity: Category) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            cursor.execute("UPDATE categorias SET nome = ? WHERE id = ?", 
                           (object_entity.name, id))
            self.conexao.commit()

            if cursor.rowcount == 0:
                return False, f"Erro: Categoria de ID {id} não encontrada"
            return True, f"Categoria #{id} ({object_entity.name}) foi atualizada com sucesso!"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: a categoria '{object_entity.name}' já existe. Verifique se está tentando duplicar uma categoria já registrada"
            return False, f"Erro ao atualizar categoria #{id}: {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"


    #metodo para listar as categorias existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todas as categorias normalmente
    def list(
            self,
            keyword=None,
            min_product_amount=0, 
            max_product_amount=10**6, 
            has_no_products=False, 
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, str, int]]:
        cursor = self.conexao.cursor()

        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "cg.id",
            "name" : "cg.nome",
            "product_amount" : "COUNT(p.id)"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para p.id
        order_column = dic_columns_bank.get(order_by_type, "cg.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        consult_sql = f"""
                    SELECT
                        cg.id AS categoria_id,
                        cg.nome AS categoria_nome,
                        COUNT(p.id) AS quantidade_produtos
                    FROM
                        categorias AS cg
                    LEFT JOIN
                        produtos AS p ON p.categoria_id = cg.id
                    WHERE 1=1
        """

        #cria parametros
        parameters: list[Any] = []

        #se keyword existir, poe keyword em parameters
        if keyword and keyword.strip():
            clause = n.build_keyword_sql_clause(["cg.nome"])
            consult_sql += f" AND {clause}"
            parameters_clause = n.build_keyword_parameters_sql(keyword, 1)
            parameters.extend(parameters_clause)

        #continua consulta
        consult_sql += """
                    GROUP BY
                        cg.id
                    HAVING
                        COUNT(p.id) >= ? AND COUNT(p.id) <= ?
        """
        
        #adciona min_product_amount e max_product_amount aos parametros
        parameters.extend([min_product_amount, max_product_amount])

        #se no_products True, acrescenta a consulta a limitacao de so pegar categorias vazias
        if has_no_products:
            consult_sql += "AND COUNT(p.id) = 0"

        #adciona order_column(order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consult_sql esta so afaltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()