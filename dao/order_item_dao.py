#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Any

from dao.base_dao import BaseDAO
from entities.order_item import OrderItem
from utils import Normalizer as n


#classe dao de orderitem
class OrderItemDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "itens_pedido"
    

    def _row_to_object(self, row) -> OrderItem:
        id, product_id, order_id, quantity, unit_price, unit_discount = row

        from dao.product_dao import ProductDAO
        prod = ProductDAO(self.conexao)
        found_product, product  = prod.find_by_id(product_id)

        from dao.order_dao import OrderDAO
        ord = OrderDAO(self.conexao)
        found_order, order = ord.find_by_id(order_id)
        
        if found_product and found_order:
            return OrderItem(product=product, order=order, id=id, quantity=quantity, unit_price=unit_price, unit_discount=unit_discount)
        elif not found_order:
            raise ValueError(f"Erro de Consistência: o item-de-pedido #{id} está relacionado a um pedido inexistente (ID {order_id})")
        raise ValueError(f"Erro de Consistência: o item #{id} (pedido #{order.id}) está relacionado a um produto inexistente (ID {product_id})")
    

    def _row_to_full_object(self, row) -> OrderItem:
        order_item = self._row_to_object(row)

        cursor = self.conexao.cursor()
        cursor.execute(f"SELECT * FROM item_pedido_lotes WHERE item_pedido_id = ?", (order_item.id,))
        lotes = cursor.fetchall()

        if lotes:
            from dao.order_item_batch_dao import OrderItemBatchDAO
            oritba = OrderItemBatchDAO(self.conexao)
            
            for lote in lotes:
                batch = oritba._row_to_full_object(lote)
                order_item.add_order_item_batch_from_db(batch)
        
        return order_item
    

    def create_new(self, object_entity: OrderItem) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            cursor.execute("""
                    INSERT INTO itens_pedido
                        (produto_id, pedido_id, quantidade, preco_unitario, desconto_unitario)
                        VALUES (?, ?, ?, ?, ?)
                        """, (object_entity.product.id, object_entity.order.id, object_entity.quantity, object_entity.unit_price, object_entity.unit_discount))
            self.conexao.commit()
            return True, f"Novo item do pedido #{object_entity.order.id} (produto {object_entity.product.name}, marca {object_entity.product.brand}) foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: Um item do produto '{object_entity.product.name}' da marca '{object_entity.product.brand}' já existe no pedido #{object_entity.order.id}. Verifique se está tentando duplicar um item já registrado"
            return False, f"Erro ao criar novo item (produto {object_entity.product.name}, marca {object_entity.product.brand}) no pedido #{object_entity.order.id}: {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: OrderItem) -> Tuple[bool, str]:
        found, item = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()

                cursor.execute("""
                        UPDATE itens_pedido 
                            SET quantidade = ?, preco_unitario = ?, desconto_unitario = ?
                            WHERE id = ?
                            """, (object_entity.quantity, object_entity.unit_price, object_entity.unit_discount, id))
                self.conexao.commit()

                return True, f"Item #{id} (pedido #{item.order.id}, produto {item.product.name}, marca {item.product.brand}) foi atualizado com sucesso!"
        
            except sqlite3.IntegrityError as e:
                return False, f"Erro ao atualizar o item #{id} (pedido #{item.order.id}, produto {item.product.name}, marca {item.product.brand}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Item-de-pedido de ID {id} não encontrado"
        

    #metodo para listar os item_pedido existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os item_pedido normalmente
    def list(
            self,
            order_id=None,
            product_id=None,
            keyword=None,
            order_date=None,
            min_quantity=0, 
            max_quantity=10**6,
            min_unit_price=0,
            max_unit_price=10**6,
            min_unit_discount=0,
            max_unit_discount=10**6,
            min_final_unit_price=0,
            max_final_unit_price=10**6,
            min_total=0,
            max_total=10**6,
            only_free=False,
            only_not_free=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, int, str, str, str, str, int, float, float, float, float]]:
        cursor = self.conexao.cursor()

        #verifica se only_free e only_not_free nao sao ambos true
        if only_free and only_not_free:
            raise ValueError("Não é possível filtrar itens por 'apenas itens gratuitos' e 'apenas itens que não são gratuitos' simultaneamente")

        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "ip.id",
            "order" : "ip.pedido_id",
            "product" : "ip.produto_id",
            "order_date" : "pd.data",
            "quantity" : "ip.quantidade",
            "unit_price" : "ip.preco_unitario",
            "unit_discount" : "ip.desconto_unitario",
            "final_unit_price" : "(ip.preco_unitario - ip.desconto_unitario)",
            "total" : "(ip.quantidade * (ip.preco_unitario - ip.desconto_unitario))"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para ip.id
        order_column = dic_columns_bank.get(order_by_type, "ip.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        #se only_free True, acrescenta a consulta a limitacao de so pegar itens gratuitos
        if only_free:
            max_total = 0

        consult_sql = f"""
                    SELECT
                        ip.id AS item_pedido_id,
                        ip.pedido_id AS pedido_id,
                        p.nome AS produto,
                        p.marca AS marca_produto,
                        cg.nome AS categoria_produto,
                        pd.data AS data_pedido,
                        ip.quantidade AS quantidade,
                        ip.preco_unitario AS preco_unidade_sem_desconto,
                        ip.desconto_unitario AS desconto_unidade,
                        (ip.preco_unitario - ip.desconto_unitario) AS preco_final_unidade,
                        (ip.quantidade * (ip.preco_unitario - ip.desconto_unitario)) AS total_item
                    FROM
                        itens_pedido AS ip
                    LEFT JOIN
                        produtos AS p ON ip.produto_id = p.id
                    LEFT JOIN
                        pedidos AS pd ON ip.pedido_id = pd.id
                    JOIN
                        categorias AS cg ON p.categoria_id = cg.id
                    WHERE
                        ip.quantidade >= ?
                        AND ip.quantidade <= ?
                        AND ip.preco_unitario >= ?
                        AND ip.preco_unitario <= ?
                        AND ip.desconto_unitario >= ?
                        AND ip.desconto_unitario <= ?
                        AND (ip.preco_unitario - ip.desconto_unitario) >= ?
                        AND (ip.preco_unitario - ip.desconto_unitario) <= ?
                        AND (ip.quantidade * (ip.preco_unitario - ip.desconto_unitario)) >= ?
                        AND (ip.quantidade * (ip.preco_unitario - ip.desconto_unitario)) <= ?
        """
        #poe os filtros numericos em parameters
        parameters: list[Any] = [min_quantity, max_quantity, min_unit_price, max_unit_price, min_unit_discount, max_unit_discount, min_final_unit_price, max_final_unit_price, min_total, max_total]
        
        #se order_id existir, poe order_id em parameters tambem
        if order_id:
            consult_sql += " AND ip.pedido_id = ?"
            parameters.append(order_id)

        #se product_id existir, poe product_id em parameters tambem
        if product_id:
            consult_sql += " AND ip.produto_id = ?"
            parameters.append(product_id)

        #se keyword existir, poe keyword em parameters tambem
        if keyword and keyword.strip():
            clause = n.build_keyword_sql_clause(["p.nome", "p.marca", "cg.nome"])
            consult_sql += f" AND {clause}"
            clause_parameters = n.build_keyword_parameters_sql(keyword, 3)
            parameters.extend(clause_parameters)

        #se order_date existir, poe order_date em parameters tambem
        if order_date:
            order_date_iso = order_date.to_iso()
            consult_sql += " AND pd.data = ?"
            parameters.append(order_date_iso)

        #se only_not_free True, acrescenta a consulta a limitacao de so pegar itens nao-gratuitos
        if only_not_free:
            consult_sql += " AND (ip.preco_unitario - ip.desconto_unitario) > 0"

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()