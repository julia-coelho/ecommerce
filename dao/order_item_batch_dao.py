#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Any

from dao.base_dao import BaseDAO
from entities.order_item_batch import OrderItemBatch
from utils import Normalizer as n


#classe dao de orderitembatch
class OrderItemBatchDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "item_pedido_lotes"
    

    def _row_to_object(self, row) -> OrderItemBatch:
        id, product_batch_id, order_item_id, quantity = row

        from dao.product_batch_dao import ProductBatchDAO
        prodbat = ProductBatchDAO(self.conexao)
        found_product_batch, product_batch  = prodbat.find_by_id(product_batch_id)

        from dao.order_item_dao import OrderItemDAO
        orditem = OrderItemDAO(self.conexao)
        found_order_item, order_item = orditem.find_by_id(order_item_id)
        
        if found_product_batch and found_order_item:
            return OrderItemBatch(product_batch=product_batch, order_item=order_item, quantity=quantity, id=id)
        elif not found_order_item:
            raise ValueError(f"Erro de Consistência: o lote-de-item-do-pedido #{id} está relacionado a um item-pedido inexistente (ID {order_item_id})")
        raise ValueError(f"Erro de Consistência: o lote-de-item #{id} (item-pedido #{order_item.id}) está relacionado a um lote inexistente (ID {product_batch_id})")
    

    def _row_to_full_object(self, row) -> OrderItemBatch:
        return self._row_to_object(row)


    def create_new(self, object_entity: OrderItemBatch) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            cursor.execute("""
                    INSERT INTO item_pedido_lotes
                        (lote_id, item_pedido_id, quantidade)
                        VALUES (?, ?, ?)
                        """, (object_entity.product_batch.id, object_entity.order_item.id, object_entity.quantity))
            self.conexao.commit()
            return True, f"Novo item-pedido-lote (item-de-pedido #{object_entity.order_item.id} - pedido #{object_entity.order_item.order.id}, produto {object_entity.order_item.product.name}, marca {object_entity.order_item.product.brand} - lote #{object_entity.product_batch.batch_number}) foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: Um lote número #{object_entity.product_batch.batch_number} do produto {object_entity.product_batch.product.name}, marca {object_entity.product_batch.product.brand} já existe no pedido #{object_entity.order_item.order.id}. Verifique se está tentando duplicar um item-pedido-lote já registrado"
            return False, f"Erro ao criar novo item-pedido-lote (item-de-pedido #{object_entity.order_item.id} - pedido #{object_entity.order_item.order.id}, produto {object_entity.order_item.product.name}, marca {object_entity.order_item.product.brand} - lote #{object_entity.product_batch.batch_number}): {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: OrderItemBatch) -> Tuple[bool, str]:
        found, batch = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()

                cursor.execute("UPDATE item_pedido_lotes SET quantidade = ? WHERE id = ?",
                            (object_entity.quantity, id))
                self.conexao.commit()
            
                return True, f"Item-pedido-lote #{id} item-pedido-lote (item-de-pedido #{batch.order_item.id} - pedido #{batch.order_item.order.id}, produto {batch.order_item.product.name}, marca {batch.order_item.product.brand} - lote #{batch.product_batch.batch_number}) foi atualizado com sucesso!"
            
            except sqlite3.IntegrityError as e:
                return False, f"Erro ao atualizar o item-pedido-lote #{id} item-pedido-lote (item-de-pedido #{batch.order_item.id} - pedido #{batch.order_item.order.id}, produto {batch.order_item.product.name}, marca {batch.order_item.product.brand} - lote #{batch.product_batch.batch_number}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Item-pedido-pedido de ID {id} não encontrado"


    #metodo para listar os item_pedido_lote existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os itens_pedido_lote normalmente
    def list(
            self,
            order_item_id=None,
            batch_id=None,
            batch_number=None,
            product_id=None,
            keyword=None,
            order_id=None,
            min_quantity=0,
            max_quantity=10**6,
            only_expired=False,
            only_valid=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, int, str, str, str, int, str, str, str, int, int, int, str]]:
        cursor = self.conexao.cursor()

        #verifica se only_expired e only_valid nao sao ambos true
        if only_expired and only_valid:
            raise ValueError("Não é possível filtrar lotes por 'apenas lotes fora da validade' e 'apenas os lotes que dentro da validade' simultaneamente")
        
        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "ipl.id",
            "order_item_id" : "ipl.item_pedido_id",
            "order_item_quantity" : "ip.quantidade",
            "batch_id" : "ipl.lote_id",
            "batch_number" : "l.numero_lote",
            "product_id" : "p.id",
            "product_name" : "p.nome",
            "order_id" : "ip.pedido_id",
            "quantity" : "quantidade"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para ipl.id
        order_column = dic_columns_bank.get(order_by_type, "ipl.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        consult_sql = f"""
                    SELECT
                        ipl.id AS item_pedido_lote_id,
                        ipl.quantidade AS item_pedido_lote_quantidade,

                        p.nome AS produto,
                        p.marca AS marca_produto,
                        cg.nome AS categoria_produto,

                        ipl.lote_id AS lote_id,
                        l.numero_lote AS numero_lote,
                        l.data_fabricacao AS data_fabricacao,
                        l.data_validade AS data_validade,

                        ipl.item_pedido_id AS item_pedido_id,
                        ip.quantidade AS item-pedido_quantidade,

                        pd.id AS pedido_id,
                        pd.data AS data_pedido

                    FROM
                        item_pedido_lotes AS ipl
                    LEFT JOIN
                        lotes AS l ON ipl.lote_id = l.id
                    JOIN
                        produtos AS p ON l.produto_id = p.id
                    LEFT JOIN
                        itens_pedido AS ip ON ipl.item_pedido_id = ip.id
                    JOIN
                        pedidos AS pd ON ip.pedido_id = pd.id
                    JOIN
                        categorias AS cg ON p.categoria_id = cg.id
                    WHERE
                        ipl.quantidade >= ?
                        AND ipl.quantidade <= ?
        """
        #poe os filtros numericos em parameters
        parameters: list[Any] = [min_quantity, max_quantity]
        
        #se order_item_id existir, poe order_item_id em parameters tambem
        if order_item_id:
            consult_sql += " AND ipl.item_pedido_id = ?"
            parameters.append(order_item_id)

        #se batch_id existir, poe batch_id em parameters tambem
        if batch_id:
            consult_sql += " AND ipl.lote_id = ?"
            parameters.append(batch_id)

        #se batch_number existir, poe batch_number em parameters tambem
        if batch_number:
            consult_sql += " AND l.numero_lote = ?"
            parameters.append(batch_number)

        #se product_id existir, poe product_id em parameters tambem
        if product_id:
            consult_sql += " AND p.id = ?"
            parameters.append(product_id)

        #se keyword existir, poe keyword em parameters tambem
        if keyword and keyword.strip:
            clause = n.build_keyword_sql_clause(["p.nome", "p.marca", "cg.nome"])
            consult_sql += f" AND {clause}"
            clause_parameters = n.build_keyword_parameters_sql(keyword, 3)
            parameters.extend(clause_parameters)

        #se order_id existir, poe order_id em parameters tambem
        if order_id:
            consult_sql += " AND pd.id = ?"
            parameters.append(order_id)

        #se only_expired True, acrescenta a consulta a limitacao de so pegar item-pedido-lotes que estão fora da validade
        if only_expired:
            consult_sql += " AND l.data_vencimento IS NOT NULL AND l.data_vencimento < Date('now')"

        #se only_valid True, acrescenta a consulta a limitacao de so pegar item-pedido-lotes que estão dentro da validade
        if only_valid:
            consult_sql += " AND l.data_vencimento IS NOT NULL AND l.data_vencimento >= Date('now')"

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()