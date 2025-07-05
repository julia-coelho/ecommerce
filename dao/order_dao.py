#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Any, Optional

from dao.base_dao import BaseDAO
from entities.order import Order
from entities import Date
from entities import PaymentStatus
from utils import Normalizer as n

#classe dao de order
class OrderDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "pedidos"
    

    def _row_to_object(self, row) -> Order:
        id, customer_id, total, full_price, global_discount, date_iso = row

        date = Date.from_iso(date_iso)
        from dao.customer_dao import CustomerDAO
        cust = CustomerDAO(self.conexao)
        found_customer, customer  = cust.find_by_id(customer_id)
        
        if found_customer:
            return Order(customer=customer, id=id, total=total, full_price=full_price, global_discount=global_discount, date=date)
        raise ValueError(f"Erro de Consistência: o pedido #{id} está relacionado a um cliente inexistente (ID {customer_id})")
    

    def _row_to_full_object(self, row) -> Order:
        order = self._row_to_object(row)

        cursor = self.conexao.cursor()
        cursor.execute(f"SELECT * FROM itens_pedido WHERE pedido_id = ?", (order.id,))
        itens = cursor.fetchall()

        if itens:
            from dao.order_item_dao import OrderItemDAO
            ordite = OrderItemDAO(self.conexao)

            for item in itens:
                item = ordite._row_to_full_object(item)
                order.add_order_item_from_db(item)

        return order


    def create_new(self, object_entity: Order) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            order_date_iso = object_entity.date.to_iso()

            cursor.execute("""
                    INSERT INTO pedidos
                        (cliente_id, total_final, total_sem_desconto, desconto_global, data)
                        VALUES (?, ?, ?, ?, ?)
                        """, (object_entity.customer.id, object_entity.total, object_entity.full_price, object_entity.global_discount, order_date_iso))
            self.conexao.commit()
            return True, f"Novo pedido (de cliente #{object_entity.customer.id}, nome {object_entity.customer.name}) foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            return False, f"Erro ao criar novo pedido (de cliente #{object_entity.customer.id}, nome {object_entity.customer.name}): {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: Order) -> Tuple[bool, str]:
        found, order = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()

                order_date_iso = object_entity.date.to_iso()

                cursor.execute("""
                        UPDATE pedidos 
                            SET total_final = ?, total_sem_desconto = ?, desconto_global = ?, data = ?
                            WHERE id = ?
                            """, (object_entity.total,  object_entity.full_price, object_entity.global_discount, order_date_iso, id))
                self.conexao.commit()

                return True, f"Pedido #{id} (cliente #{order.customer.id}, nome {order.customer.name}) foi atualizado com sucesso!"
            
            except sqlite3.IntegrityError as e:
                return False, f"Erro ao atualizar o pedido {order.id} (cliente #{order.customer.id}, nome {order.customer.name}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Pedido de ID {id} não encontrado"


    #metodo para listar os pedidos existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os pedidos normalmente
    def list(
            self,
            customer_id=None,
            person_keyword=None,
            date=None,
            date_before=None,
            date_after=None,
            payment_status=None,
            min_total=0,
            max_total=10**6,
            min_full_price=0,
            max_full_price=10**6,
            min_global_discount=0,
            max_global_discount=10**6,
            min_quantity=0,
            max_quantity=10**6,
            has_payment=False,
            only_not_paid=False,
            only_pending_payment=False,
            only_free=False,
            only_not_free=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, int, str, str, int, int, Optional[float], Optional[float], Optional[float], Optional[str], Optional[str], Optional[str], Optional[str]]]:
        cursor = self.conexao.cursor()

        #verifica se only_free e only_not_free nao sao ambos true
        if only_free and only_not_free:
            raise ValueError("Não é possível filtrar pedidos por 'apenas pedidos gratuitos' e 'apenas pedidos que não são gratuitos' simultaneamente")
        
        #verifica se only_free e only_pending_payment nao sao ambos true
        if only_free and only_pending_payment:
            raise ValueError("Não é possível filtrar pedidos por 'apenas pedidos gratuitos' e 'apenas pedidos cujo pagamento está em status pendente' simultaneamente, pois pedidos gratuitos não têm pagamentos")
        
        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "pd.id",
            "customer_id" : "pd.cliente_id",
            "customer_name" : "c.nome",
            "total" : "pd.total_final",
            "full_price" : "pd.total_sem_desconto",
            "global_discount" : "pd.desconto_global",
            "date" : "pd.data"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para pd.id
        order_column = dic_columns_bank.get(order_by_type, "pd.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        if only_free:
            max_total = 0

        consult_sql = f"""
                    SELECT
                        pd.id AS pedido_id,
                        pd.cliente_id AS cliente_id,
                        c.nome AS cliente,
                        pd.data AS data_pedido_feito,
                        COUNT(ip.id) AS quantidade_produtos_diferentes,
                        SUM(ip.quantidade) AS quantidade_itens,

                        pd.total_sem_desconto AS preco_sem_desconto,
                        pd.desconto_global AS desconto_total,
                        pd.total_final AS preco_total,

                        pg.status AS status_pagamento,
                        pg.tipo AS tipo_pagamento,
                        pg.data_pagamento AS data_pagamento,
                        pg.pagador_nome AS responsavel_pagamento_nome

                    FROM
                        pedidos AS pd
                    LEFT JOIN
                        clientes AS c ON pd.cliente_id = c.id
                    LEFT JOIN
                        pagamentos AS pg
                        ON pg.id = (
                            SELECT id FROM pagamentos AS pg2
                            WHERE pg2.pedido_id = pd.id
                            ORDER BY pg2.data_pagamento DESC
                            LIMIT 1)
                    LEFT JOIN
                        itens_pedido AS ip ON ip.pedido_id = pd.id
                    WHERE
                        pd.total_sem_desconto >= ?
                        AND pd.total_sem_desconto <= ?
                        AND pd.desconto_global >= ?
                        AND pd.desconto_global <= ?
                        AND pd.total_final >= ?
                        AND pd.total_final <= ?
        """
        #poe os filtros numericos em parameters
        parameters: list[Any] = [min_full_price, max_full_price, min_global_discount, max_global_discount, min_total, max_total]
        
        #se customer_id existir, poe customer_id em parameters tambem
        if customer_id:
            consult_sql += " AND pd.cliente_id = ?"
            parameters.append(customer_id)

        #se person_keyword existir, poe person_keyword em parameters tambem
        if person_keyword and person_keyword.strip():
            clause = n.build_keyword_sql_clause(["c.nome", "pg.pagador_nome"])
            consult_sql += f" AND {clause}"
            clause_parameters = n.build_keyword_parameters_sql(person_keyword, 2)
            parameters.extend(clause_parameters)
            
        #se date existir, poe date em parameters tambem
        if date:
            date_iso = date.to_iso()
            consult_sql += " AND pd.data = ?"
            parameters.append(date_iso)

        #se date_before existir, poe date_before em parameters tambem
        if date_before:
            date_before_iso = date_before.to_iso()
            consult_sql += " AND pd.data <= ?"
            parameters.append(date_before_iso)

        #se date_after existir, poe date_after em parameters tambem
        if date_after:
            date_after_iso = date_after.to_iso()
            consult_sql += " AND pd.data >= ?"
            parameters.append(date_after_iso)

        #se only_pending_payment True, acrescenta a consulta a limitacao de so pegar pedidos cujo pagamento esta pendente
        if only_pending_payment:
            payment_status = PaymentStatus.PENDING

        #se payment_status existir, poe payment_status em parameters tambem
        if payment_status:
            consult_sql += " AND pg.status = ?"
            parameters.append(payment_status)

        #se has_payment True, acrescenta a consulta a limitacao de so pegar pedidos que sao relacionados a pelo menos um pagamento
        if has_payment:
            consult_sql += " AND pg.id IS NOT NULL"

        #se only_not_paid True, acrescenta a consulta a limitacao de so pegar pedidos que nao sao relacionados a nenhum pagamento de status 'pago'
        if only_not_paid:
            consult_sql += """ 
                AND NOT EXISTS (
                    SELECT 1 FROM pagamentos AS pg3
                    WHERE pg3.pedido_id = pd.id AND pg3.status = 'pago'
                )
        """
            
        #se only_not_free True, acrescenta a consulta a limitacao de so pegar pedidos que nao sao gratuitos
        if only_not_free:
            consult_sql += " AND pd.total_final > 0"

        #poe max_quantity e min_quantity em parameters
        consult_sql += """ GROUP BY
                            pd.id,
                            pd.cliente_id,
                            c.nome,
                            pd.data,
                            pd.total_sem_desconto,
                            pd.desconto_global,
                            pd.total_final,
                            pg.status,
                            pg.tipo,
                            pg.data_pagamento,
                            pg.pagador_nome
                        HAVING 
                            SUM(ip.quantidade) >= ? 
                            AND SUM(ip.quantidade) <= ?
        """

        parameters.extend([min_quantity, max_quantity])

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()