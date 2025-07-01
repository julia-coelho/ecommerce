#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Optional, Any

from dao.base_dao import BaseDAO
from entities.product_batch import ProductBatch
from entities import Date
from utils import Normalizer as n

#classe dao de product_batch
class ProductBatchDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "lotes"
    

    def _row_to_object(self, row) -> ProductBatch:
        id, product_id, batch_number, manufacturing_date_iso, due_date_iso, quantity = row

        manufacturing_date = Date.from_iso(manufacturing_date_iso)
        if due_date_iso is not None:
            due_date = Date.from_iso(due_date_iso)
        else:
            due_date = None

        from dao.product_dao import ProductDAO
        prod = ProductDAO(self.conexao)
        found, product = prod.find_by_id(product_id)
        if found:
            return ProductBatch(product=product, batch_number=batch_number, manufacturing_date=manufacturing_date, quantity=quantity, id=id, due_date=due_date)
        raise ValueError(f"Erro de Consistência: o lote de ID {id}, número de lote #{batch_number}, é de um produto inexistente (ID {product_id})")


    def _row_to_full_object(self, row) -> ProductBatch:
        return self._row_to_object(row)


    def create_new(self, object_entity: ProductBatch) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            manufacturing_date_iso = object_entity.manufacturing_date.to_iso()
            if object_entity.due_date:
                due_date_iso = object_entity.due_date.to_iso()
            else:
                due_date_iso = None
            cursor.execute("""
                    INSERT INTO lotes
                        (produto_id, numero_lote, data_fabricacao, quantidade, data_vencimento)
                        VALUES (?, ?, ?, ?, ?)
                        """, (object_entity.product.id, object_entity.batch_number, manufacturing_date_iso, object_entity.quantity, due_date_iso))
            self.conexao.commit()
            return True, f"Novo lote #{object_entity.batch_number} do produto {object_entity.product.name}, marca {object_entity.product.brand}, foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: O lote número #{object_entity.batch_number} do produto {object_entity.product.name}, marca {object_entity.product.brand}, já existe. Verifique se está tentando duplicar um lote já registrado"
            return False, f"Erro ao criar novo lote (lote número #{object_entity.batch_number} do produto {object_entity.product.name}, marca {object_entity.product.brand}): {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: ProductBatch) -> Tuple[bool, str]:
        found, batch = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()

                cursor.execute("UPDATE lotes SET quantidade = ? WHERE id = ?",
                            (object_entity.quantity, id))
                self.conexao.commit()

                return True, f"Lote de ID {id} (lote número #{batch.batch_number} do produto {batch.product.name}, marca {batch.product.brand}) foi atualizado com sucesso!"
            
            except sqlite3.IntegrityError as e:
                return False, f"Erro ao atualizar o lote de ID {id} (lote número #{batch.batch_number} do produto {batch.product.name}, marca {batch.product.brand}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Lote de ID {id} não encontrado"


    #metodo para listar os lotes existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os lotes normalmente
    def list(
            self,
            product_id=None,
            keyword=None,
            manufacturing_date=None,
            due_date=None, 
            min_quantity=0, 
            max_quantity=10**6,
            only_inventory=False,
            only_expired=False,
            only_valid=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, str, str, str, str, int, str, Optional[str], bool]]:
        cursor = self.conexao.cursor()

        #verifica se only_expired e only_valid nao sao ambos true
        if only_expired and only_valid:
            raise ValueError("Não é possível filtrar lotes por 'apenas lotes fora da validade' e 'apenas os lotes que dentro da validade' simultaneamente")
        
        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "l.id",
            "batch_number" : "l.numero_lote",
            "product" : "p.nome",
            "brand" : "p.marca",
            "quantity" : "l.quantidade",
            "manufacturing_date" : "l.data_fabricacao",
            "due_date" : "l.data_vencimento"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para l.id
        order_column = dic_columns_bank.get(order_by_type, "l.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        consult_sql = f"""
                    SELECT
                        l.id AS lote_id,

                        p.nome AS produto,
                        p.marca AS produto_marca,
                        cg.nome AS categoria_produto,
                        
                        l.numero_lote AS numero_lote,
                        l.quantidade AS lote_quantidade,
                        l.data_fabricacao AS data_fabricacao,
                        l.data_vencimento AS data_validade,
                    CASE
                        WHEN l.data_vencimento IS NOT NULL AND l.data_vencimento < DATE('now') THEN 1
                        ELSE 0
                    END AS vencido
                    FROM
                        lotes AS l
                    LEFT JOIN
                        produtos AS p ON l.produto_id = p.id
                    JOIN
                        categorias AS cg ON p.categoria_id = cg.id
                    WHERE
                        l.quantidade >= ?
                        AND l.quantidade <= ?
        """
        #poe os filtros numericos em parameters
        parameters: list[Any] = [min_quantity, max_quantity]

        #se product_id existir, poe product_id em parameters tambem
        if product_id:
            consult_sql += " AND l.produto_id = ?"
            parameters.append(product_id)

        #se keyword existir, poe keyword em parameters tambem
        if keyword and keyword.strip():
            clause = n.build_keyword_sql_clause(["p.nome", "p.marca", "cg.nome"])
            consult_sql += f" AND {clause}"
            clause_parameters = n.build_keyword_parameters_sql(keyword, 3)
            parameters.extend(clause_parameters)

        #se manufacturing_date existir, poe manufacturing_date em parametros tambem
        if manufacturing_date:
            manufacturing_date_iso = manufacturing_date.to_iso()
            consult_sql += " AND l.data_fabricacao = ?"
            parameters.append(manufacturing_date_iso)

        #se due_date existir, poe due_date em parameters tambem
        if due_date:
            due_date_iso = due_date.to_iso()
            consult_sql += " AND l.data_vencimento = ?"
            parameters.append(due_date_iso)

        #se only_expired True, acrescenta a consulta a limitacao de so pegar lotes fora da validade
        if only_expired:
            consult_sql += " AND l.data_vencimento IS NOT NULL AND l.data_vencimento < Date('now')"

        #se only_valid True, acrescenta a consulta a limitacao de so pegar lotes dentro da validade
        if only_valid:
            consult_sql += " AND l.data_vencimento IS NOT NULL AND l.data_vencimento >= Date('now')"

        #se only_inventory True, acrescenta a consulta a limitacao de so pegar lotes com exemplar no estoque
        if only_inventory:
            consult_sql += " AND l.quantidade > 0"

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()