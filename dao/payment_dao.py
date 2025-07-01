#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Optional, Any

from dao.base_dao import BaseDAO
from entities.payment import Payment
from entities import Date
from utils import Normalizer as n

#classe dao de payment
class PaymentDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "pagamentos"
    

    def _row_to_object(self, row) -> Payment:
        id, order_id, total, payment_type, status, transaction_id, payment_date_iso, payer, account_identifier = row

        if payment_date_iso:
            payment_date = Date.from_iso(payment_date_iso)
        else:
            payment_date=None

        from dao.order_dao import OrderDAO
        ord = OrderDAO(self.conexao)
        found, order = ord.find_by_id(order_id)
        if found:
            return Payment(order=order, type=payment_type, transaction_id=transaction_id, payer_name=payer, account_identifier=account_identifier, id=id, status=status, payment_date=payment_date, total=total)
        raise ValueError(f"Erro de Consistência: o pagamento #{id} está relacionado a um pedido inexistente (ID {order_id})")
    

    def _row_to_full_object(self, row) -> Payment:
        return self._row_to_object(row)
    

    def create_new(self, object_entity: Payment) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            if object_entity.payment_date:
                payment_date_iso = object_entity.payment_date.to_iso()
            else:
                payment_date_iso = None
            cursor.execute("""
                    INSERT INTO pagamentos
                        (pedido_id, total, tipo, status, transacao_id, data_pagamento, pagador_nome, endereco_conta)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (object_entity.order.id, object_entity.total, object_entity.type, object_entity.status, object_entity.transaction_id, payment_date_iso, object_entity.payer, object_entity.account_identifier))
            self.conexao.commit()
            return True, f"Novo pagamento #{object_entity.transaction_id}, do pedido #{object_entity.order.id}, foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: Já existe um pagamento com a transação '{object_entity.transaction_id}'. Verifique se está tentando duplicar um pagamento já registrado."
            return False, f"Erro ao criar novo pagamento (pagamento #{object_entity.transaction_id}, do pedido #{object_entity.order.id}): {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: Payment) -> Tuple[bool, str]:
        found, payment = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()

                if object_entity.payment_date:
                    payment_date_iso = object_entity.payment_date.to_iso()
                else:
                    payment_date_iso = None

                cursor.execute("UPDATE pagamentos SET status = ?, data_pagamento = ? WHERE id = ?",
                            (object_entity.status, payment_date_iso, id))
                self.conexao.commit()

                return True, f"Pagamento de ID {id} (pagamento #{payment.transaction_id}, do pedido #{payment.order.id}) foi atualizado com sucesso!"
            
            except sqlite3.IntegrityError as e:
                if "UNIQUE constraint failed" in str(e):
                    return False, f"Erro: O pagamento de transação_id #{payment.transaction_id} já existe. Verifique se está tentando duplicar um pagamento já registrado"
                return False, f"Erro ao atualizar o pagamento de ID {id} (pagamento #{payment.transaction_id}, do pedido #{payment.order.id}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Pagamento de ID {id} não encontrado"


    #metodo para listar os pagamentos existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os pagamentos normalmente
    def list(
            self,
            order_id=None,
            type=None,
            status=None,
            customer_id=None,
            person_name=None,
            payment_date=None,
            payment_date_before=None,
            payment_date_after=None,
            order_date=None,
            min_total=0, 
            max_total=10**6,
            only_not_paid=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, int, str, int, str, float, str, str, str, Optional[str], str, str]]:
        cursor = self.conexao.cursor()
        
        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "pg.id",
            "type" : "pg.tipo",
            "status" : "pg.status",
            "payment_date" : "pg.data_pagamento",
            "order" : "pg.pedido_id",
            "order_date" : "pd.data"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para pg.id
        order_column = dic_columns_bank.get(order_by_type, "pg.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        consult_sql = f"""
                    SELECT
                        pg.id AS pagamento_id,
                        pg.pedido_id AS pedido_id,
                        pd.data AS data_pedido,
                        pd.cliente_id AS cliente_id,
                        c.nome AS cliente,
                        pg.total AS total,
                        pg.tipo AS tipo_pagamento,
                        pg.status AS status_pagamento,
                        pg.transacao_id AS transacao_id,
                        pg.data_pagamento AS data_pagamento_efetuado,
                        pg.endereco_conta AS endereco_conta,
                        pg.pagador_nome AS responsavel_pagamento_nome
                    FROM
                        pagamentos AS pg
                    LEFT JOIN
                        pedidos AS pd ON pg.pedido_id = pd.id
                    JOIN
                        clientes AS c ON pd.cliente_id = c.id
                    WHERE
                        pg.total >= ?
                        AND pg.total <= ?
        """
        #poe os filtros numericos em parameters
        parameters: list[Any] = [min_total, max_total]
        
        #se order_id existir, poe order_id em parameters tambem
        if order_id:
            consult_sql += " AND pg.pedido_id = ?"
            parameters.append(order_id)

        #se type existir, poe type em parameters tambem
        if type:
            consult_sql += " AND pg.tipo = ?"
            parameters.append(type)   

        #se status existir, poe status em parameters tambem
        if status:
            consult_sql += " AND pg.status = ?"
            parameters.append(status)   

        #se customer_id existir, poe customer_id em parameters tambem
        if customer_id:
            consult_sql += " AND pd.cliente_id = ?"
            parameters.append(customer_id)          
            
        #se person_name existir, poe person_name em parameters tambem
        if person_name and person_name.strip():
            clause = n.build_keyword_sql_clause(["c.nome", "pg.pagador_nome"])
            consult_sql += f" AND {clause}"
            clause_parameters = n.build_keyword_parameters_sql(person_name, 2)
            parameters.extend(clause_parameters)

        #se payment_date existir, poe payment_date em parametros tambem
        if payment_date:
            payment_date_iso = payment_date.to_iso()
            consult_sql += " AND pg.data_pagamento IS NOT NULL AND pg.data_pagamento = ?"
            parameters.append(payment_date_iso)

        #se payment_date_before existir, poe payment_date_before em parametros tambem
        if payment_date_before:
            payment_date_before_iso = payment_date_before.to_iso()
            consult_sql += " AND pg.data_pagamento IS NOT NULL AND pg.data_pagamento <= ?"
            parameters.append(payment_date_before_iso)

        #se payment_date_after existir, poe payment_date_after em parametros tambem
        if payment_date_after:
            payment_date_after_iso = payment_date_after.to_iso()
            consult_sql += " AND pg.data_pagamento IS NOT NULL AND pg.data_pagamento >= ?"
            parameters.append(payment_date_after_iso)

        #se order_date existir, poe order_date em parametros tambem
        if order_date:
            order_date_iso = order_date.to_iso()
            consult_sql += " AND pd.data = ?"
            parameters.append(order_date_iso)

        #se only_not_paid True, acrescenta a consulta a limitacao de so pegar pagamentos que (ainda) não foram pagos
        if only_not_paid:
            consult_sql += " AND pg.status != 'pago'"

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()