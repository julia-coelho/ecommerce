#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo

def test_order():
    """teste da classe-entidade Order"""

    from entities import Date, Category, Product
    from entities.address import Address
    from entities.customer import Customer
    from entities.order import Order
    from entities.order_item import OrderItem
    from entities.payment import Payment
    from entities.payment_type import PaymentType
    from entities.payment_status import PaymentStatus

    print("\n========================")
    print(" Testes da classe Order ")
    print("========================\n")

    # objetos auxiliares
    cat = Category(name="Remédios", id=1)
    prod = Product(name="Paracetamol", brand="NeoQuímica", category=cat, unit_price=20.0, id=101)
    melhor_dia = Date(9, 3, 1998)
    hoje = Date.today()
    endereco = Address("70000-000", "DF", "Brasília", "Asa Norte", "Rua A", "10")
    cliente = Customer("Paciente Zero", "paz@email.com", "hash123", Date(1,1,1990), "61999999999", endereco, id=1)

    #construtor
    print("\n Testes do Construtor\n")

    #testes positivos
    pedido_v1 = teste_construtor(lambda: Order(customer=cliente), "Order com apenas customer (OK esperado)")
    pedido_v2 = teste_construtor(lambda: Order(customer=cliente, id=10), "Order com customer e id, apenas (OK esperado)")
    pedido_v3 = teste_construtor(lambda: Order(customer=cliente, id=20, total=0.0), "Order com total=0.0, sem full_price e sem global_discount (OK esperado)")
    pedido_v4 = teste_construtor(lambda: Order(customer=cliente, id=30, full_price=0.0), "Order com full_price=0.0, sem total e sem global_discount (OK esperado)")
    pedido_v5 = teste_construtor(lambda: Order(customer=cliente, id=40, global_discount=0.0), "Order com global_discount=0.0, sem total e sem full_price (OK esperado)")
    pedido_v6 = teste_construtor(lambda: Order(customer=cliente, id=50, total=15.0, full_price=15.0), "Order com full_price válido > 0.0, total=full_price e sem global_discount (OK esperado)")
    pedido_v7 = teste_construtor(lambda: Order(customer=cliente, id=60, total=15.0, full_price=15.0, global_discount=0.0), "Order com full_price válido > 0.0, total=full_price e global_discount=0.0 (OK esperado)")
    pedido_v8 = teste_construtor(lambda: Order(customer=cliente, id=70, total=14.0, full_price=15.0, global_discount=1.0), "Order com full_price válido > 0.0, global_discount válido>0.0 e total=(full_price - global_discount) (OK esperado)")
    pedido_v9 = teste_construtor(lambda: Order(customer=cliente, id=80, date=melhor_dia), "Order com apenas customer e date (OK esperado)")
    pedido_v10 = teste_construtor(lambda: Order(customer=cliente, id=90, total=140.0, full_price=150.0, global_discount=10.0, date=melhor_dia), "Order  válida dados completos (customer, id, total, full_price, global_discount e date) (OK esperado)")
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    teste_construtor(lambda: Order(customer=cliente, id="um"), "Order com id=str (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=0), "Order com id=0 (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=-1), "Order com id negativo (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=3.5), "Order com id=float (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=object()), "Order com id=object (ERRO esperado)")
    print("\n")

    # testes negativos - customer
    teste_construtor(lambda: Order(customer="cliente"), "Order com customer=str (ERRO esperado)")
    teste_construtor(lambda: Order(customer=123), "Order com customer=int (ERRO esperado)")
    teste_construtor(lambda: Order(customer=object()), "Order com customer=object (ERRO esperado)")
    teste_construtor(lambda: Order(customer=None), "Order com customer=None (ERRO esperado)")
    teste_construtor(lambda: Order(), "Order sem customer (ERRO esperado)")
    print("\n")

    # testes negativos - total (atributo opcional)
    teste_construtor(lambda: Order(customer=cliente, total=-1.0), "Order com total negativo (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, total="100"), "Order com total=str (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, total=object()), "Order com total=object (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, total=None), "Order com total=None (ERRO esperado)")
    print("\n")

    # testes negativos - full_price (atributo opcional)
    teste_construtor(lambda: Order(customer=cliente, full_price=-5.0), "Order com full_price negativo (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, full_price="200"), "Order com full_price str (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, full_price=object()), "Order com full_price object (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, full_price=None), "Order com full_price=None (ERRO esperado)")
    print("\n")

    # testes negativos - global_discount (atributo opcional)
    teste_construtor(lambda: Order(customer=cliente, global_discount=-10), "Order com global_discount negativo (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, global_discount="20"), "Order com global_discount=str (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, global_discount=object()), "Order com global_discount=object (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, global_discount=None), "Order com global_discount=None (ERRO esperado)")
    print("\n")

    # testes negativos - date (atributo opcional)
    teste_construtor(lambda: Order(customer=cliente, date="ontem"), "Order com date=str (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, date=123), "Order com date=int (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, date=object()), "Order com date=object (ERRO esperado)")
    print("\n")

    #teste positivo - logica entre total, full_price e global_discount correta
    teste_construtor(lambda: Order(customer=cliente, id=140, total=-5.0, full_price=15.0, global_discount=20.0), "Order com global_discount > full_price, full_price válido > 0.0 e total=(full_price - global_discount) (OK esperado)")
    print("\n")

    #testes negativos - logica entre total, full_price e global_discount errada
    teste_construtor(lambda: Order(customer=cliente, id=110, total=15.0), "Order com total válido > 0.0, sem full_price e sem global_discount (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=120, full_price=15.0), "Order com full_price válido > 0.0, sem total (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=130, global_discount=15.0), "Order com global_discount válido > 0.0, sem total e sem full_price (ERRO esperado)")
    teste_construtor(lambda: Order(customer=cliente, id=150, total=15.0, full_price=12.0, global_discount=1.0), "Order com full_price válido>0.0, global_discount válido>0.0 e total != (full_price - global_discount) (ERRO esperado)")
    print("\n")


    #metodos
    print("\n Testes dos Métodos\n")
    if pedido_v10 and pedido_v1 and pedido_v6 and pedido_v7:
        # criar pedido com item e desconto para testar consistência
        pedido_complete = pedido_v10
        item = OrderItem(product=prod, order=pedido_complete, quantity=2, unit_price=20.0, unit_discount=5.0, id=1)
        pedido_complete.add_order_item(item)
        pagamento = Payment(order=pedido_complete, type=PaymentType.PIX, transaction_id="TX123", payer_name="Paciente Zero", account_identifier="CPF123")
        pedido_complete.payment = pagamento
        pedido_min = pedido_v1

        # __str__
        teste_metodo(lambda: str(pedido_min), "__str__() de Order válida com dados mínimos (sem id, sem passar total, sem passar full_price, sem passar global_discount, sem passar date) (order com id=None, total=0.0 e payment.status='GRATUITO' esperado)")
        teste_metodo(lambda: str(pedido_complete), "__str__() de Order válida com dados completos (com id, com total explicitamente passado, com full_price explicitamente passado, com global_discount explicitamente passado, com date explicitamente passado, com payment e com itens populada) (order com id=90, total=170.0 e payment.status='pendente' esperado)")
        print("\n")

        # __eq__
        pedido = Order(customer=cliente, id=1)
        pedido_igual = Order(customer=cliente, id=1)
        pedido_diferente = Order(customer=cliente, id=2)
        pedido_sem_id = Order(customer=cliente)

        teste_metodo(lambda: pedido == pedido_igual, "__eq__() com id igual (True esperado)")
        teste_metodo(lambda: pedido == pedido_diferente, "__eq__() com id diferente (False esperado)")
        teste_metodo(lambda: pedido == pedido_sem_id, "__eq__() com um Order sem id (False esperado)")
        teste_metodo(lambda: pedido == 'string', "__eq__() Order X string (False esperado)")
        teste_metodo(lambda: pedido == object(), "__eq__() Order X Object (False esperado)")
        teste_metodo(lambda: pedido == None, "__eq__() Order X None (False esperado)")
        print("\n")

        # get_formatted_total()
        teste_metodo(lambda: pedido_min.get_formatted_total(), "get_formatted_total() de Order válida com dados mínimos (sem id, sem passar total, sem passar full_price, sem passar global_discount, sem passar date) ('R$ 0.00' esperado)")
        teste_metodo(lambda: pedido_complete.get_formatted_total(), "get_formatted_total() de Order válida com dados completos (com id, com total explicitamente passado, com full_price explicitamente passado, com global_discount explicitamente passado, com date explicitamente passado, com payment e com itens populada) ('R$ 170.00' esperado)")
        print("\n")

        # get_customer_email()
        teste_metodo(lambda: pedido.get_customer_email(), "get_customer_email() de Order válida ('paz@email.com' esperado)")
        print("\n")

        # add_order_discount() (positivos)
        pedido_desconto = Order(customer=cliente, id=999, total=20.0, full_price=25.0, global_discount=5.0)
        teste_metodo(lambda: pedido_desconto.add_order_discount(2.0), "add_order_discount() com desconto válido (OK esperado)")

        # add_order_discount() (negativos)
        teste_metodo(lambda: pedido_desconto.add_order_discount("2.0"), "add_order_discount() com desconto tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: pedido_desconto.add_order_discount(object()), "add_order_discount() com desconto tipo inválido object (ERRO esperado)")
        teste_metodo(lambda: pedido_desconto.add_order_discount(-5.0), "add_order_discount() com desconto negativo (ERRO esperado)")
        teste_metodo(lambda: pedido_desconto.add_order_discount(100.0), "add_order_discount() com desconto excedendo full_price (ERRO esperado)")
        print("\n")

        # add_order_item() (positivos)
        item_valido = OrderItem(product=prod, order=pedido_complete, quantity=1, unit_price=10.0, unit_discount=2.0, id=101)
        teste_metodo(lambda: pedido_complete.add_order_item(item_valido), "add_order_item() com item válido (OK esperado)")

        # add_order_item() (negativos)
        item_erro_pedido = OrderItem(product=prod, order=Order(customer=cliente, id=200), quantity=1, unit_price=10.0, unit_discount=1.0, id=102)
        teste_metodo(lambda: pedido.add_order_item("string"), "add_order_item() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: pedido.add_order_item(3), "add_order_item() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: pedido.add_order_item(object()), "add_order_item() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: pedido.add_order_item(None), "add_order_item() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: pedido.add_order_item(), "add_order_item() sem argumento (ERRO esperado)")
        teste_metodo(lambda: pedido.add_order_item(item_erro_pedido), "add_order_item() com item válido, mas inconsistente (de outra Order) (ERRO esperado)")
        print("\n")

        # add_order_item_from_db() (positivos)
        pedido_db = Order(customer=cliente, id=300, total=40.0, full_price=50.0, global_discount=10.0)
        item_db1 = OrderItem(product=prod, order=pedido_db, quantity=1, unit_price=20.0, unit_discount=5.0, id=103)
        item_db2 = OrderItem(product=prod, order=pedido_db, quantity=1, unit_price=15.0, unit_discount=5.0, id=104)
        item_db3 = OrderItem(product=prod, order=pedido_db, quantity=1, unit_price=15.0, unit_discount=7.0, id=105)
        item_db4 = OrderItem(product=prod, order=pedido_db, quantity=1, unit_price=20.0, unit_discount=0.0, id=105)

        teste_metodo(lambda: pedido_db.add_order_item_from_db(item_db1), "add_order_item_from_db() com item válido 1 (OK esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(item_db2), "add_order_item_from_db() com item válido 2 (OK esperado)")

        # add_order_item_from_db() (negativos)
        teste_metodo(lambda: pedido_db.add_order_item_from_db(item_db3), "add_order_item_from_db() com desconto acumulado excedendo global_discount (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(item_db4), "add_order_item_from_db() com total acumulado excedendo total e total sem desconto acumulado excedendo full_price (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db("string"), "add_order_item()_from_db com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(3), "add_order_item()_from_db com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(object()), "add_order_item()_from_db com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(None), "add_order_item()_from_db com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(), "add_order_item()_from_db sem argumento (ERRO esperado)")
        teste_metodo(lambda: pedido_db.add_order_item_from_db(item_erro_pedido), "add_order_item()_from_db com item válido, mas inconsistente (de outra Order) (ERRO esperado)")
        print("\n")

        # get_payment_status()
        teste_metodo(lambda: pedido.get_payment_status(), "get_payment_status() de Order válida com total=0.0 (e sem payment, obrigatoriamente) ('GRATUITO' esperado)")
        teste_metodo(lambda: pedido_v6.get_payment_status(), "get_payment_status() de Order válida com total>0.0 e sem payment ('Pagamento não iniciado' esperado)")
        teste_metodo(lambda: pedido_complete.get_payment_status(), "get_payment_status() de Order válida com payment válido (pendente) ('pendente' esperado)")
        print("\n")

        # set_payment() (positivos)
        pagamento_pago = Payment(order=pedido_v6, type=PaymentType.PIX, transaction_id="TX124", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido_v6.total, status=PaymentStatus.PAID)
        pagamento_pendente = Payment(order=pedido_v6, type=PaymentType.PIX, transaction_id="TX142", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido_v6.total)
        pagamento_pedido_errado = Payment(order=pedido_v7, type=PaymentType.PIX, transaction_id="TX369", payer_name="Paciente Zero", account_identifier="CPF123", total=pedido_v7.total)
        pagamento_total_errado = Payment(order=pedido_v6, type=PaymentType.PIX, transaction_id="TX124", payer_name="Paciente Zero", account_identifier="CPF123", total=100.0)
        teste_metodo(lambda: pedido_v6.set_payment(pagamento_pendente), "set_payment() com payment válido, payment é da Order, total de pagamento é igual ao total da Order e diferente de 0 e status do pagamento é pendente (OK esperado)")

        # set_payment() (negativos)
        teste_metodo(lambda: pedido_v6.set_payment("pagamento inválido"), "set_payment() com payment inválido (tipo inválido: string) (ERRO esperado)")
        teste_metodo(lambda: pedido_v6.set_payment(pagamento_pedido_errado), "set_payment() com payment válido, mas não é daquela Order (ERRO esperado)")
        teste_metodo(lambda: pedido.set_payment(pagamento_total_errado), "set_payment() com payment válido, mas total do pagamento é diferente do total da Order (ERRO esperado)")
        teste_metodo(lambda: pedido.set_payment(pagamento), "set_payment() com payment válido, com total do pagamento igual ao total da Order, mas esse total é 0 (ERRO esperado)")
        teste_metodo(lambda: pedido_v6.set_payment(pagamento_pago), "set_payment() com payment válido, payment é da Order, total de pagamento é igual ao total da Order e diferente de 0, mas status do payment não é 'pendente' (ERRO esperado)")
        print("\n")

        # validate_order() (positivos)
        teste_metodo(lambda: Order.validate_order(pedido_min), "validate_order() com objeto Order válido mínimo (sem id, sem passar total, sem passar full_price, sem passar global_discount, sem passar date, sem payment, com atributo-lista items vazia) (OK esperado)")
        teste_metodo(lambda: Order.validate_order(pedido_complete), "validate_order() com objeto Order completo (com id, com total explicitamente passado, com full_price explicitamente passado, com global_discount explicitamente passado, com date explicitamente passado, com payment e com itens populada com 2 OrderItem diferentes) (OK esperado)")

        # validate_order() (negativos)
        teste_metodo(lambda: Order.validate_order("str"), "validate_order() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: Order.validate_order(123), "validate_order() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: Order.validate_order(object()), "validate_order() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: Order.validate_order(None), "validate_order() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: Order.validate_order(), "validate_order() sem argumento (ERRO esperado)")
        print("\n")
