#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3
from typing import Tuple, List, Any

from dao.base_dao import BaseDAO
from entities.customer import Customer
from entities import Date
from entities import Address
from utils import Normalizer as n


#classe dao de customer
class CustomerDAO(BaseDAO):
    def __init__(self, conexao) -> None:
        super().__init__(conexao)
    

    def _get_table(self) -> str:
        return "clientes"
    

    def _row_to_object(self, row) -> Customer:
        id, name, email, password_hash, birthday_iso, phone, address_string_bank, register_date_iso = row

        birthday = Date.from_iso(birthday_iso)
        address = Address.from_string(address_string_bank)
        register_date = Date.from_iso(register_date_iso)

        return Customer(id=id, name=name, email=email, password_hash=password_hash, birthday=birthday, phone=phone, address=address, register_day=register_date)


    def _row_to_full_object(self, row) -> Customer:
        customer = self._row_to_object(row)

        cursor = self.conexao.cursor()
        cursor.execute(f"SELECT * FROM pedidos WHERE cliente_id = ?", (customer.id,))
        pedidos = cursor.fetchall()

        if pedidos:
            from dao.order_dao import OrderDAO
            ord = OrderDAO(self.conexao)

            for pedido in pedidos:
                order = ord._row_to_full_object(pedido)
                customer.add_order(order)

        return customer


    def create_new(self, object_entity: Customer) -> Tuple[bool, str]:
        try:
            cursor = self.conexao.cursor()

            birthday_iso = object_entity.birthday.to_iso()
            address_string_bank = object_entity.address.to_string_bank()
            register_date_iso = object_entity.register_day.to_iso()

            cursor.execute("""
                    INSERT INTO clientes
                        (nome, email, senha_hash, aniversario, telefone, endereco, data_cadastro)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """, (object_entity.name, object_entity.email, object_entity.password_hash, birthday_iso, object_entity.phone, address_string_bank, register_date_iso))
            self.conexao.commit()
            return True, f"Novo cliente (nome {object_entity.name}, e-mail {object_entity.email}) foi criado com sucesso"
        
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed" in str(e):
                return False, f"Erro: Um cliente com e-mail '{object_entity.email}' já existe. Verifique se está tentando duplicar um cliente já registrado"
            return False, f"Erro ao criar novo cliente (nome {object_entity.name}, e-mail {object_entity.email}): {e}"
        except sqlite3.Error as e:
            return False, f"Erro Inesperado: {e}"
    

    def update_by_id(self, id: int, object_entity: Customer) -> Tuple[bool, str]:
        found, customer = self.find_by_id(id)
        if found:
            try:
                cursor = self.conexao.cursor()

                birthday_iso = object_entity.birthday.to_iso()
                address_string_bank = object_entity.address.to_string_bank()

                cursor.execute("""
                        UPDATE clientes 
                            SET nome = ?, email = ?, senha_hash = ?, aniversario = ?, telefone = ?, endereco = ?
                            WHERE id = ?
                            """, (object_entity.name, object_entity.email, object_entity.password_hash, birthday_iso, object_entity.phone, address_string_bank, id))
                self.conexao.commit()

                return True, f"Cliente #{id} (nome {object_entity.name}, e-mail {object_entity.email}) foi atualizado com sucesso!"
            
            except sqlite3.IntegrityError as e:
                return False, f"Erro ao atualizar o cliente #{customer.id} (nome {customer.name}, e-mail{customer.email}): {e}"
            except sqlite3.Error as e:
                return False, f"Erro Inesperado: {e}"
        return False, f"Erro: Cliente de ID {id} não encontrado"


    #metodo para listar os clientes existentes no banco, com filtros e ordenando de formas diferentes:
    #se chamar so list(), lista todos os clientes normalmente
    def list(
            self,
            person_keyword=None,
            birthday=None,
            register_date=None,
            register_date_before=None,
            register_date_after=None,
            last_order_before=None,
            last_order_after=None,
            address_part=None,
            min_age = 0,
            max_age = 200,
            min_orders=0,
            max_orders=10**6,
            min_total_spent=0,
            max_total_spent=10**6,
            min_avg_spent=0,
            max_avg_spent=10**6,
            has_payment_pending=False,
            has_disputed_payment=False,
            order_by_type="id", 
            asc_or_desc="ASC"
    ) -> List[Tuple[int, str, str, int, str, str, str, int, float, float, str, float, float]]:
        cursor = self.conexao.cursor()
        
        #dicionario para traduzir order_by_type em opcoes validas para o banco
        dic_columns_bank = {
            "id" : "c.id",
            "name" : "c.nome",
            "email" : "c.email",
            "age": "strftime('%Y', 'now') - strftime('%Y', c.aniversario) - (strftime('%m-%d', 'now') < strftime('%m-%d', c.aniversario))",
            "register_date" : "c.data_cadastro",
            "last_order_date" : "MAX(pd.data)",
            "amount_orders" : "COUNT(pd.id)",
            "total_spent" : "SUM(pd.total_final)",
            "avg_spent_per_order" : "COALESCE(SUM(pd.total_final)/NULLIF(COUNT(pd.id), 0), 0)",
            "min_order_value" : "MIN(pd.total_final)",
            "max_order_value" : "MAX(pd.total_final)"
        }

        #estabelece quais sao as direcoes validas para order_by_type
        valid_directions = ["ASC", "DESC"]

        #traduz order_by_type conforme o dicionario dic_columns_bank, caso nao exista traducao possivel, traduz para pd.id
        order_column = dic_columns_bank.get(order_by_type, "c.id")

        #verifica se asc_or_desc eh uma direcao valida, se nao for, transforma em ASC
        if asc_or_desc in valid_directions:
            direction = asc_or_desc
        else:
            direction = "ASC"

        consult_sql = f"""
                    SELECT
                        c.id AS cliente_id,
                        c.nome AS nome,
                        c.email AS email,
                        strftime('%Y', 'now') - strftime('%Y', c.aniversario) - (strftime('%m-%d', 'now') < strftime('%m-%d', c.aniversario)) AS idade,
                        c.telefone AS telefone,
                        c.endereco AS endereco,
                        c.data_cadastro AS data_cadastro,

                        COUNT(pd.id) AS quantidade_pedidos_feitos,
                        SUM(pd.total_final) AS total_gasto,
                        COALESCE(SUM(pd.total_final)/NULLIF(COUNT(pd.id), 0), 0) AS media_gasto_por_pedido,
                        MAX(pd.data) AS ultimo_pedido_data,
                        MIN(pd.total_final) AS total_pedido_mais_barato,
                        MAX(pd.total_final) AS total_pedido_mais_caro
                    FROM
                        clientes AS c
                    LEFT JOIN
                        pedidos AS pd ON pd.cliente_id = c.id
                    LEFT JOIN
                        pagamentos AS pg ON pg.pedido_id = pd.id
                    WHERE 1=1
        """

        #cria lista parameters vazia
        parameters: list[Any] = []

        #se person_keyword existir, poe person_keyword em parameters
        if person_keyword and person_keyword.strip():
            clause = n.build_keyword_sql_clause(["c.nome", "c.email"])
            parameters_clause = n.build_keyword_parameters_sql(person_keyword, 2)
            consult_sql += f" AND {clause}"
            parameters.extend(parameters_clause)

        #se birthday existir, poe birthday em parameters tambem
        if birthday:
            birthday_iso = birthday.to_iso()
            consult_sql += " AND c.aniversario = ?"
            parameters.append(birthday_iso)

        #se register_date existir, poe register_date em parameters tambem
        if register_date:
            register_date_iso = register_date.to_iso()
            consult_sql += " AND c.data_cadastro = ?"
            parameters.append(register_date_iso)

        #se register_date_before existir, poe register_date_before em parameters tambem
        if register_date_before:
            register_date_before_iso = register_date_before.to_iso()
            consult_sql += " AND c.data_cadastro <= ?"
            parameters.append(register_date_before_iso)

        #se register_date_after existir, poe register_date_after em parameters tambem
        if register_date_after:
            register_date_after_iso = register_date_after.to_iso()
            consult_sql += " AND c.data_cadastro >= ?"
            parameters.append(register_date_after_iso)

        #se address_part existir, poe address_part em parameters
        if address_part:
            address_part_param = f"%{address_part.lower()}%"
            consult_sql += " AND (LOWER(c.endereco) LIKE ?)"
            parameters.append(address_part_param)

        #se has_payment_pending existir, poe has_payment_pending em parameters tambem
        if has_payment_pending:
            consult_sql += """
            AND EXISTS (
                SELECT 1 FROM pedidos AS pd2
                JOIN pagamentos AS pg2 ON pd2.id = pg2.pedido_id
                WHERE pd2.cliente_id = c.id AND pg2.status = 'pendente'
            )
        """

        #se has_disputed_payment existir, poe has_disputed_payment em parameters tambem
        if has_disputed_payment:
            consult_sql += """
            AND EXISTS (
                SELECT 1 FROM pedidos AS pd2
                JOIN pagamentos AS pg2 ON pd2.id = pg2.pedido_id
                WHERE pd2.cliente_id = c.id AND pg2.status = 'em disputa'
            )
        """

        consult_sql += """ 
        GROUP BY
            c.id,
            c.nome,
            c.email,
            c.telefone,
            c.endereco,
            c.data_cadastro
        """

        #poe os filtros numericos em parameters
        having = """
                    HAVING
                        COUNT(pd.id) >= ?
                        AND COUNT(pd.id) <= ?
                        AND SUM(pd.total_final) >= ?
                        AND SUM(pd.total_final) <= ?
                        AND COALESCE(SUM(pd.total_final)/NULLIF(COUNT(pd.id), 0), 0) >= ?
                        AND COALESCE(SUM(pd.total_final)/NULLIF(COUNT(pd.id), 0), 0) <= ?
                        AND strftime('%Y', 'now') - strftime('%Y', c.aniversario) - 
                        (strftime('%m-%d', 'now') < strftime('%m-%d', c.aniversario)) >= ?
                        AND strftime('%Y', 'now') - strftime('%Y', c.aniversario) - 
                        (strftime('%m-%d', 'now') < strftime('%m-%d', c.aniversario)) <= ?
        """
        
        parameters.extend([min_orders, max_orders, min_total_spent, max_total_spent, min_avg_spent, max_avg_spent, min_age, max_age])

        #se last_order_before existir, poe last_order_before em parameters tambem
        if last_order_before:
            last_order_before_iso = last_order_before.to_iso()
            having += " AND MAX(pd.data) <= ?"
            parameters.append(last_order_before_iso)

        #se last_order_after existir, poe last_order_after em parameters tambem
        if last_order_after:
            last_order_after_iso = last_order_after.to_iso()
            having += " AND MAX(pd.data) >= ?"
            parameters.append(last_order_after_iso)

        consult_sql += having

        #adciona order_column (order_by_type validada) e direction (asc_or_desc validada) a consult_sql
        #ou seja, adciona ordenacao segura
        #consulta sql esta so faltando os parametros
        consult_sql += f" ORDER BY {order_column} {direction}"

        #cursor.execute automaticamente acrescenta a lista de parametros e roda a consulta, tudo junto
        cursor.execute(consult_sql, parameters)

        #retorna uma lista de tuplas com todos os itens do select
        return cursor.fetchall()