#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_metodo_by_id_dao, get_cust, teste_metodo
from utils import Normalizer as n

def test_customer_dao(conexao):

    from dao.customer_dao import CustomerDAO
    from dao.order_dao import OrderDAO
    from dao.payment_dao import PaymentDAO
    from entities.customer import Customer
    from entities import Address, Date, PaymentType, PaymentStatus
    from entities.order import Order
    from entities.payment import Payment

    print("\n==============================")
    print(" Testes da classe CustomerDAO ")
    print("==============================\n")

    dao = CustomerDAO(conexao)
    order_dao = OrderDAO(conexao)


    # funções auxiliares

    def print_list_customers(filters):
        try:
            resultado = dao.list(**filters)
            if not resultado:
                print("[OK] list() retornou lista vazia")
            else:
                print("\n----------------------------------------------------------------------------------------------- LISTA DE CLIENTES -----------------------------------------------------------------------------------------------")
                print("{:<13} {:<30} {:<21} {:<8} {:<13} {:<14} {:<14} {:<13} {:<13} {:<13} {:<15} {:<16} {:<10}".format(
                    "ID", "Nome", "E-mail", "Idade", "Telefone", "Endereço(CEP)", "Data Cadastro", "Num. Pedidos", "Total Gasto", "Média Pedido", "Último Pedido", "Pedido +Barato", "Pedido +Caro"
                ))
                print("-" * 210)
                for c in resultado:
                    id_, nome, email, idade, tel, end, data_cad, quantidade, total, media, ultimo, preco_mais_barato, preco_mais_caro = c
                    
                    # tratamento de valores para evitar erro de formatacao
                    endereco = Address.from_string(end)
                    quantidade = quantidade if quantidade is not None else 0
                    total = total if total is not None else 0
                    media = media if media is not None else 0
                    ultimo = ultimo or "   ---   "
                    preco_mais_barato = preco_mais_barato if preco_mais_barato is not None else 0
                    preco_mais_caro = preco_mais_caro if preco_mais_caro is not None else 0

                    print(f"{id_:<3} {nome:<29} {email:<33} {idade:<4} {tel:<18} {endereco.cep:<13} {data_cad:<18} {quantidade:<10} R$ {total:<10.2f} R$ {media:<10.2f} {ultimo:<17} R$ {preco_mais_barato:<12.2f} R$ {preco_mais_caro:<8.2f}")
                print("\n")
        except Exception as e:
            print(f"[ERRO Exception] list() -> {e}\n")

    # garantindo enderecos validos
    anita_malfatti_address = Address(cep="09910190", state="SP", city="Diadema", district="Centro", street="Rua Washington Luiz", number="56", complement="Apto 405")
    anita_malfatti_address_2 = Address(cep="09911020", state="SP", city="Diadema", district="Centro", street="Rua Sao Joaquim", number="57")
    pinacoteca_address = Address(cep="01120010", state="SP", city="São Paulo", district="Luz", street="Praça da Luz", number="2")
    valid_address = Address(cep="11111111", state="MG", city="Cidade", district="Bairro", street="Rua", number="00")
    

    # testes de create_new()
    print("\nTestes de create_new()")
    teste_metodo_by_id_dao(lambda: dao.create_new(Customer(name="Anita Catarina Malfatti", email="malfatti@pintura.com", password_hash="ohomemamarelo", birthday=Date(2, 12, 1912), phone="(11)88888-8888", address=anita_malfatti_address)), "create_new com cliente válido com dados mínimos (sem id e sem register_day passado explicitamente) (novo cliente Anita Catarina Malfatti, e-mail malfatti@pintura.com, esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Customer(name="Ramos de Azevedo", email="razevedo@arquitetura.com", password_hash="modernismo", birthday=Date(8, 12, 1851), phone="(11)63324-1000", address=pinacoteca_address, id=2, register_day=Date(24, 12, 1905))), "create_new com cliente válido com dados completos (com id e com register_day passado explicitamente) (novo cliente Ramos Azevedo, e-mail razevedo@arquitetura.com.br, esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Customer(name="Anita Malfatti", email="malfatti@pintura.com", password_hash="ohomemamarelo", birthday=Date(2, 12, 1889), phone="(11)88888-8888", address=anita_malfatti_address)), "create_new duplicado (ERRO esperado)")

    # testes de update_by_id()
    print("\nTestes de update_by_id()")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(1, Customer(name="Anita Malfatti", email="amalfatti@expressionismo.com", password_hash="aestudanterussa", birthday=Date(2, 12, 1889), phone="(11)99999-9999", address=anita_malfatti_address_2)), "update_by_id válido (Cliente de ID 1 Anita Malfatti, e-mail amalfatti@expressionismo.com, atualizado esperado)")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(99, Customer(name="Pessoa Pessoa", email="pessoa@pessoas.com", password_hash="1234", birthday=Date(1, 1, 2001), phone="(11)95555-5555", address=valid_address)), "update_by_id com ID inexistente (ERRO esperado)")

    # testes de delete_by_id()
    print("\nTestes de delete_by_id()")
    teste_metodo_by_id_dao(lambda: dao.create_new(Customer(name="Pessoa Temporaria", email="temp@pessoas.com", password_hash="12345", birthday=Date(31, 12, 1999), phone="(11)93333-3333", address=valid_address)), "novo cliente Pessoa Temporaria, e-mail temp@pessoas.com, criado")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(3), "delete_by_id com dados (id) válido (delete de 'ID 3' esperado)")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(999), "delete_by_id inexistente (ERRO esperado)")

    # testes de find_by_id()
    print("\nTestes de find_by_id()")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(1), "find_by_id com dado (id) válido (Cliente de ID 1 Anita Malfatti, e-mail amalfatti@expressionismo.com, esperado)")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(99), "find_by_id com ID inexistente (ERRO esperado)")

    # testes de find_by_id_full_object()
    print("\nTestes de find_by_id_full_object()")
    teste_metodo_by_id_dao(lambda: dao.find_by_id_full_object(1), "find_by_id_full_object com dado (id) válido e sem pedidos (cliente Anita de Malfatti, e-mail malfatti@pintura.com, esperado)")
    ramos_azevedo = get_cust(conexao, 2)
    order_r1 = Order(customer=ramos_azevedo, date=Date(12, 9, 1911))
    order_r2 = Order(customer=ramos_azevedo, total=191.5, full_price=191.6, global_discount=0.1, date=Date(25, 1, 1933))
    teste_metodo_by_id_dao(lambda: order_dao.create_new(order_r1), "novo pedido (ID 1) de cliente Ramos de Azevedo, e-mail razevedo@arquitetura.com.br")
    teste_metodo_by_id_dao(lambda: order_dao.create_new(order_r2), "novo pedido (ID 2) de cliente Ramos de Azevedo, e-mail razevedo@arquitetura.com.br")
    teste_metodo_by_id_dao(lambda: dao.find_by_id_full_object(2), "find_by_id_full_object com dado (id) válido e com pedidos (cliente Ramos de Azevedo, e-mail razevedo@arquitetura.com.br, com 2 pedidos, esperado)")
    found, customer = dao.find_by_id_full_object(2)
    if found:
        ramos_azevedo = customer
        print("Pedidos de Ramos de Azevedo:")
        print(f"Pedido 1 de Ramos de Azevedo: {ramos_azevedo.orders[0]}")
        print(f"Pedido 2 de Ramos de Azevedo: {ramos_azevedo.orders[1]}")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(99), "find_by_id_full_object com ID inexistente (ERRO esperado)")

    # testes de outros metodos
    print("\n _get_table() testada indiretamente pelos testes de delete_by_id() e find_by_id()")
    print("\n _row_to_object() testada indiretamente pelos testes de find_by_id()")
    print("\n _row_to_full_object() testada indiretamente pelos testes de find_by_id_full_object()")

    print("\n")
    while True:
        answer = input(f"\nGostaria de seguir para os testes do método list() de CustomerDAO? São 21 testes. Recomenda-se fazer os testes do método list() de CustomerDAO em uma janela cheia do terminal, com letra pequena.\n")
        answer = n.normalize(answer)
        if answer=="SIM":
            # testes de list()
            print("\nTestes de list()")

            # cria clientes distintos para testes de list()
            dao.create_new(Customer(name="Oswald de Andrade", email="oswald@semanadaarte.com.br", password_hash="marcozero", birthday=Date(11, 1, 1890), phone="(11)98888-8888", address=valid_address, register_day=Date(19, 3, 1908)))
            dao.create_new(Customer("Tarsila do Amaral", "tarsila@pinturabrasil.com", "oabaporu", Date(1, 9, 1886), "(11)97777-7777", valid_address, register_day=Date(4, 8, 1921)))
            tarsila_amaral = get_cust(conexao, 5)
            dao.create_new(Customer("Mario de Andrade", "mandrade@artebrasil.com", "macunaima", Date(9, 10, 1893), "(11)96666-6666", valid_address, register_day=Date(3, 6, 1914)))
            dao.create_new(Customer("Menotti Del Picchia", "picchia@artebrasil.com", "assis", Date(20, 3, 1892), "(11)95555-5555", valid_address))
            dao.create_new(Customer("Carlos Drummond de Andrade", "drummond@escrita.org", "rosapovo", Date(31, 10, 1902), "(11)94444-4444", valid_address))
            dao.create_new(Customer("Heitor Villa-Lobos", "villalobos@teatronacional.com.br", "bachianas!brasil", Date(5, 3, 1887), "(11)93333-3333", valid_address, register_day=Date(13, 2, 1922)))
            villa_lobos = get_cust(conexao, 9)
            dao.create_new(Customer("Antonio de Alcantara Machado", "alcantara@escritamoderna.org", "novelas_paulistanas", Date(25, 5, 1901), "(11)92222-2222", valid_address))
            
            #criar pedidos distintos para testes de list()
            order_dao.create_new(Order(customer=tarsila_amaral, total=2500.0, full_price=2500.0, date=Date(12, 1, 1928)))
            order_dao.create_new(Order(customer=tarsila_amaral, total=150.0, full_price=205.0, global_discount=55.0, date=Date(1, 5, 1933)))
            order_dao.create_new(Order(customer=ramos_azevedo, total=190.0, full_price=190.0, date=Date(29, 4, 1924)))
            order_dao.create_new(Order(customer=villa_lobos, total=193.0, full_price=195.5, global_discount=2.5, date=Date(8, 4, 1930)))
            order_dao.create_new(Order(customer=villa_lobos, total=80.0, full_price=90.0, global_discount=10.0, date=Date(19, 5, 1950)))
            order_dao.create_new(Order(customer=villa_lobos, date=Date(30, 6, 1954)))

            #criar pagamentos distintos para testes de list()
            pay_dao = PaymentDAO(conexao)
            found, order_t1 = order_dao.find_by_id(3)
            if found:
                pay_dao.create_new(Payment(order=order_t1, type=PaymentType.CREDITO, transaction_id="abc", payer_name="Tarsila do Amaral", account_identifier="9999", status=PaymentStatus.PAID, payment_date=Date(12, 2, 1928)))
            found, order_t2 = order_dao.find_by_id(4)
            if found:
                pay_dao.create_new(Payment(order=order_t2, type=PaymentType.DEBITO, transaction_id="def", payer_name="Tarsila do Amaral", account_identifier="9999"))
            found, order_r3 = order_dao.find_by_id(5)
            if found:
                pay_dao.create_new(Payment(order=order_r3, type=PaymentType.BOLETO, transaction_id="boletoX", payer_name="Ramos de Azevedo", account_identifier="8888", status=PaymentStatus.DISPUTED, payment_date=Date(27, 9, 1911)))
            found, order_vl1 = order_dao.find_by_id(6)
            if found:
                pay_dao.create_new(Payment(order=order_vl1, type=PaymentType.PAYPAL, transaction_id="paypal1", payer_name="Heitor Villa-Lobos", account_identifier="villalobos@teatronacional.com.br", status=PaymentStatus.PENDING))

            print("\nNovos clientes, novos pedidos e novos pagamentos para popular tabelas criados")

            i=1
            filters = dict()

            print(f"\n[{i}] list() sem filtros (lista populada esperada)")
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] person_keyword='amaral' (lista com único cliente 'Tarsila do Amaral' esperada)")
            filters = dict(person_keyword="amaral")
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] birthday='9/10/2025' (lista com único cliente 'Mario de Andrade' esperada)")
            filters = dict(birthday=Date(9, 10, 2025))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] register_date=today (lista com 4 clientes esperada)")
            filters = dict(register_date=Date.today())
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] register_date_before='1/1/1920' (lista com 3 clientes esperada)")
            filters = dict(register_date_before=Date(1, 1, 1920))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] register_date_before='1/1/1920' e register_date_after='1/1/1910' (lista com único cliente 'Mario de Andrade' esperada)")
            filters = dict(register_date_before=Date(1, 1, 1920), register_date_after=Date(1, 1, 1910))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] register_date_before='1/1/1910' e register_date_after='1/1/1920' (ERRO esperado)")
            filters = dict(register_date_before=Date(1, 1, 1910), register_date_after=Date(1, 1, 1920))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] last_order_before='1/1/1940' (lista com 2 clientes esperada)")
            filters = dict(last_order_before=Date(1, 1, 1940))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] last_order_before='1/1/1940' e last_order_after='1/4/1933' (lista com único cliente 'Tarsila do Amaral' esperada)")
            filters = dict(last_order_before=Date(1, 1, 1940), last_order_after=Date(1, 4, 1933))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] last_order_before='1/1/1930' e last_order_after='1/1/1940' (ERRO esperado)")
            filters = dict(last_order_before=Date(1, 1, 1930), last_order_after=Date(1, 1, 1940))
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] address_part='diadema' (lista com único cliente 'Anitta Malfatti' esperada)")
            filters = dict(address_part='diadema')
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_age=125 (lista com 7 clientes esperada)")
            filters = dict(min_age=125)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_age=125, max_age=135 (lista com 4 clientes esperada)")
            filters = dict(min_age=125, max_age=135)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_orders=1 (lista com 3 clientes esperada)")
            filters = dict(min_orders=1)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_orders=1, max_orders=2 (lista com único cliente 'Tarsila do Amaral' esperada)")
            filters = dict(min_orders=1, max_orders=2)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_total_spent=300 (lista com 2 clientes esperada)")
            filters = dict(min_total_spent=300)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_total_spent=300, max_total_spent=1000 (lista com único cliente 'Ramos de Azevedo' esperada)")
            filters = dict(min_total_spent=300, max_total_spent=1000)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_avg_spent=1 (lista com 3 clientes esperada)")
            filters = dict(min_avg_spent=1)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] min_avg_spent=1, max_avg_spent=100 (lista com único cliente 'Heitor Villa-Lobos' esperada)")
            filters = dict(min_avg_spent=1, max_avg_spent=100)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] has_payment_pending=True (lista com 2 clientes esperada)")
            filters = dict(has_payment_pending=True)
            print_list_customers(filters)
            i += 1

            print(f"\n[{i}] has_disputed_payment=True (lista com único cliente 'Ramos de Azevedo' esperada)")
            filters = dict(has_disputed_payment=True)
            print_list_customers(filters)
            i += 1

            while True:
                answer = input(f"\nGostaria de seguir para os testes de ordenação do método list() de CustomerDAO? São 22 testes. A recomendação de fazer os testes do método list() de CustomerDAO em uma janela cheia do terminal, com letra pequena, continua.\n")
                answer = n.normalize(answer)
                if answer=="SIM":
                    # ordenações
                    for column in ["id", "name", "email", "age", "register_date", "last_order_date", "amount_orders", "avg_spent_per_order", "min_order_value", "max_order_value"]:
                        for direction in ["ASC", "DESC"]:
                            print(f"\n[{i}] list() ordenada por {column} na direção {direction}")
                            filters = dict(order_by_type=f'{column}', asc_or_desc=f'{direction}')
                            print_list_customers(filters)
                            i+=1

                    print(f"\n[{i}] list() com ordenação por coluna inválida (lista ordenada por coluna id ASC esperada)")
                    filters = dict(order_by_type='order')
                    print_list_customers(filters)
                    i+=1


                    print(f"\n[{i}] list() com ordenação por direção inválida (lista ordenada por id em direção ascendente esperada)")
                    filters = dict(asc_or_desc='crescente')
                    print_list_customers(filters)
                    i+=1
                    return
                elif answer=="NAO":
                    return
        elif answer=="NAO":
            return
        print("\nPor favor, insira uma resposta válida.\n")
    

