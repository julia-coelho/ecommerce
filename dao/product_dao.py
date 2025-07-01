#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Any

from dao.base_dao import BaseDAO
from entities import Product
from utils import Normalizer as n

#classe dao de product
class ProductDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "produtos"
    

    def _row_to_object(self, row) -> Product:
        id, name, brand, category_id, unit_price, unit_discount = row

        from dao.category_dao import CategoryDAO
        cat = CategoryDAO(self.conexao)
        found, category = cat.find_by_id(category_id)
        
        if found:
            return Product(name=name, brand=brand, category=category, unit_price=unit_price, id=id, unit_discount=unit_discount)
        raise ValueError(f"Erro de Consistência: o produto '{name}', da marca '{brand}', é de uma categoria inexistente (ID {category_id})")
    

    def _row_to_full_object(self, row) -> Product:
        return self._row_to_object(row)


    def create_new(self, object_entity: Product) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            cursor.execute("""
                    INSERT INTO produtos
                        (nome, marca, categoria_id, preco_unitario, desconto_unitario)
                        VALUES (?, ?, ?, ?, ?)
                        """, (object_entity.name, object_entity.brand, object_entity.category.id, object_entity.unit_price, object_entity.unit_discount))
            self.conexao.commit()
            return True, f"Novo produto '{object_entity.name}' da marca '{object_entity.brand}' foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: O produto '{object_entity.name}' da marca '{object_entity.brand}' já existe. Verifique se está tentando duplicar um produto já registrado"
            return False, f"Erro ao criar novo produto '{object_entity.name}' da marca '{object_entity.brand}': {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: Product) -> Tuple[bool, str]:
        found, product = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()


                cursor.execute("""
                        UPDATE produtos 
                            SET marca = ?, categoria_id = ?, preco_unitario = ?, desconto_unitario = ?
                            WHERE id = ?
                            """, (object_entity.brand, object_entity.category.id, object_entity.unit_price, object_entity.unit_discount, id))
                self.conexao.commit()

                return True, f"Produto #{id} ({product.name}, marca {object_entity.brand}) foi atualizado com sucesso!"
                
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    return False, f"Erro ao atualizar o produto '{product.name}' da marca '{product.brand}' para a marca {object_entity.brand}: já existe outro produto chamado '{product.name}' da marca '{object_entity.brand}'"
                return False, f"Erro ao atualizar produto #{id} ({product.name}, marca {product.brand}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Produto de ID {id} não encontrado"


    #metodo para listar os produtos existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os produtos normalmente
    def list(
            self,
            keyword=None,
            category_id=None,
            min_unit_price=0, 
            max_unit_price=10**6, 
            min_unit_discount=0,
            max_unit_discount=10**6,
            min_final_unit_price=0,
            max_final_unit_price=10**6,
            min_quantity=0,
            max_quantity=10**6,
            only_inventory=False,
            no_inventory=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, str, str, str, float, float, float, int]]:
        cursor = self.conexao.cursor()

        #verifica se no_inventory e only_inventory nao sao ambos true
        if no_inventory and only_inventory:
            raise ValueError("Não é possível filtrar produtos por 'apenas produtos em estoque' e 'apenas produtos que não estão em estoque' simultaneamente")

        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "p.id",
            "name" : "p.nome",
            "brand" : "p.marca",
            "category" : "cg.nome",
            "unit_price" : "p.preco_unitario",
            "unit_discount" : "p.desconto_unitario",
            "final_unit_price" : "(p.preco_unitario - p.desconto_unitario)",
            "quantity" : "SUM(l.quantidade)"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para p.id
        order_column = dic_columns_bank.get(order_by_type, "p.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        consult_sql = f"""
                    SELECT
                        p.id AS produto_id,
                        p.nome AS produto,
                        p.marca AS produto_marca,
                        cg.nome AS categoria_nome,
                        p.preco_unitario AS preco_sem_desconto,
                        p.desconto_unitario AS desconto,
                        (p.preco_unitario - p.desconto_unitario) AS preco_final,
                        COALESCE(SUM(l.quantidade), 0) AS quantidade_estoque

                    FROM
                        produtos AS p
                    JOIN
                        categorias AS cg ON p.categoria_id = cg.id
                    LEFT JOIN
                        lotes AS l ON p.id = l.produto_id
                    WHERE
                        p.preco_unitario >= ?
                        AND p.preco_unitario <= ?
                        AND p.desconto_unitario >= ?
                        AND p.desconto_unitario <= ?
                        AND (p.preco_unitario - p.desconto_unitario) >= ?
                        AND (p.preco_unitario - p.desconto_unitario) <= ?
        """
        #poe os filtros numericos em parameters
        parameters: list[Any] = [min_unit_price, max_unit_price, min_unit_discount, max_unit_discount, min_final_unit_price, max_final_unit_price]

        #se keyword existir, poe keyword em parameters tambem
        if keyword and keyword.strip():
            clause = n.build_keyword_sql_clause(["p.nome", "p.marca", "cg.nome"])
            consult_sql += f" AND {clause}"
            clause_parameters = n.build_keyword_parameters_sql(keyword, 3)
            parameters.extend(clause_parameters)

        #se category_id existir, poe category_id em parametros tambem
        if category_id:
            consult_sql += " AND cg.id = ?"
            parameters.append(category_id)

        #se only_inventory True, acrescenta a consulta a limitacao de so pegar produtos com exemplar no estoque
        if only_inventory:
            min_quantity = 1

        #se no_inventory True, acrescenta a consulta a limitacao de so pegar produtos com nenhum exemplar no estoque
        if no_inventory:
            max_quantity = 0

        #poe max_quantity e min_quantity em parameters
        consult_sql += """ GROUP BY
                            p.id,
                            p.nome,
                            p.marca,
                            cg.nome,
                            p.preco_unitario,
                            p.desconto_unitario
                        HAVING 
                            COALESCE(SUM(l.quantidade), 0) >= ? 
                            AND COALESCE(SUM(l.quantidade), 0) <= ?"""

        parameters.extend([min_quantity, max_quantity])

        #agora todos os parametros estao em parametros

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()
