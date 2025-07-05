#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo


def test_customer():
    """teste da classe-entidade Customer"""

    from entities.customer import Customer
    from entities import Date
    from entities import Address
    from entities.order import Order

    # testes de Customer
    print("\n===========================")
    print(" Testes da classe Customer ")
    print("===========================\n")

    # objetos auxiliares
    valid_date = Date(1, 1, 2000)
    valid_address = Address("12345-678", "SP", "São Paulo", "Centro", "Rua A", "123")
    valid_register_day = Date(2, 2, 2020)

    #construtor
    print("\n Testes do Construtor")

    # testes positivos do construtor
    valid_customer_min = teste_construtor(
        lambda: Customer(
            name="Bob",
            email="bobby@email.com",
            password_hash="senhaSegura123",
            birthday=valid_date,
            phone="11999999999",
            address=valid_address
        ),
        "Customer válido com dados mínimos (sem id e sem register_day passado explicitamente) (OK esperado)"
    )

    valid_customer = teste_construtor(
        lambda: Customer(
            name="Donna Madonna",
            email="donnadodona@email.com",
            password_hash="outraSenhaSegura",
            birthday=valid_date,
            phone="(21)98888-7777",
            address=valid_address,
            id=2,
            register_day=valid_register_day
        ),
        "Customer válido com dados mínimos (com id e com register_day passado explicitamente) (OK esperado)"
    )
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        birthday=valid_date, phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(id="um", **base_kwargs), "Customer com id=str (ERRO esperado)")
    teste_construtor(lambda: Customer(id=0, **base_kwargs), "Customer com id=0 (ERRO esperado)")
    teste_construtor(lambda: Customer(id=-1, **base_kwargs), "Customer com id negativo (ERRO esperado)")
    teste_construtor(lambda: Customer(id=3.14, **base_kwargs), "Customer com id=float (ERRO esperado)")
    teste_construtor(lambda: Customer(id=object(), **base_kwargs), "Customer com id=object (ERRO esperado)")
    print("\n")
    
    # testes negativos - name
    base_kwargs = dict(
        email="teste@email.com", password_hash="senha", birthday=valid_date,
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(name=None, **base_kwargs), "Customer com name=None (ERRO esperado)")
    teste_construtor(lambda: Customer(name=123, **base_kwargs), "Customer com name=int (ERRO esperado)")
    teste_construtor(lambda: Customer(name=3.14, **base_kwargs), "Customer com name=float (ERRO esperado)")
    teste_construtor(lambda: Customer(name=object(), **base_kwargs), "Customer com name=object (ERRO esperado)")
    teste_construtor(lambda: Customer(name="", **base_kwargs), "Customer com name vazio (ERRO esperado)")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem name (ERRO esperado)")
    print("\n")

    # testes negativos - email
    base_kwargs = dict(
        name="Joao", password_hash="senha", birthday=valid_date,
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(email=None, **base_kwargs), "Customer com email=None (ERRO esperado)")
    teste_construtor(lambda: Customer(email="sem_arroba.com", **base_kwargs), "Customer com email malformado (ERRO esperado)")
    teste_construtor(lambda: Customer(email="sem_extensao@a.", **base_kwargs), "Customer com email malformado (ERRO esperado)")
    teste_construtor(lambda: Customer(email="sem_extensao@a", **base_kwargs), "Customer com email malformado (ERRO esperado)")
    teste_construtor(lambda: Customer(email="", **base_kwargs), "Customer com email vazio (ERRO esperado)")
    teste_construtor(lambda: Customer(email=123, **base_kwargs), "Customer com email=int (ERRO esperado)")
    teste_construtor(lambda: Customer(email=12.3, **base_kwargs), "Customer com email=float (ERRO esperado)")
    teste_construtor(lambda: Customer(email=object(), **base_kwargs), "Customer com email=object (ERRO esperado)")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem email (ERRO esperado)")
    print("\n")

    # testes negativos - password_hash
    base_kwargs = dict(
        name="Joao", email="teste@email.com", birthday=valid_date,
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(password_hash=None, **base_kwargs), "Customer com password_hash=None (ERRO esperado)")
    teste_construtor(lambda: Customer(password_hash="", **base_kwargs), "Customer com password_hash vazio (ERRO esperado)")
    teste_construtor(lambda: Customer(password_hash=123, **base_kwargs), "Customer com password_hash=int (ERRO esperado)")
    teste_construtor(lambda: Customer(password_hash=12.3, **base_kwargs), "Customer com password_hash=float (ERRO esperado)")
    teste_construtor(lambda: Customer(password_hash=object(), **base_kwargs), "Customer com password_hash=object (ERRO esperado)")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem password_hash (ERRO esperado)")
    print("\n")

    # testes negativos - birthday
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(birthday=None, **base_kwargs), "Customer com birthday=None (ERRO esperado)")
    teste_construtor(lambda: Customer(birthday="01-01-2000", **base_kwargs), "Customer com birthday=str inválido (ERRO esperado)")
    teste_construtor(lambda: Customer(birthday="2000-01-01", **base_kwargs), "Customer com birthday=str inválido (mas formato ISO válido) (ERRO esperado)")
    teste_construtor(lambda: Customer(birthday="", **base_kwargs), "Customer com birthday str vazio (ERRO esperado)")
    teste_construtor(lambda: Customer(birthday=object(), **base_kwargs), "Customer com birthday=object (ERRO esperado)")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem birthday (ERRO esperado)")
    print("\n")

    # testes negativos - phone
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        birthday=valid_date, address=valid_address
    )
    teste_construtor(lambda: Customer(phone=123, **base_kwargs), "Customer com phone=int (ERRO esperado)")
    teste_construtor(lambda: Customer(phone=3.14, **base_kwargs), "Customer com phone=float (ERRO esperado)")
    teste_construtor(lambda: Customer(phone="abcdefghijk", **base_kwargs), "Customer com phone com letras (ERRO esperado)")
    teste_construtor(lambda: Customer(phone="(61) 9999-999", **base_kwargs), "Customer com phone com poucos dígitos (ERRO esperado)")
    teste_construtor(lambda: Customer(phone="619999999999", **base_kwargs), "Customer com phone com dígitos demais (ERRO esperado)")
    teste_construtor(lambda: Customer(phone=None, **base_kwargs), "Customer com phone=None (ERRO esperado)")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items() if k != 'phone'}), "Customer sem phone (ERRO esperado)")
    print("\n")

    # testes negativos - address
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        birthday=valid_date, phone="11999999999"
    )
    teste_construtor(lambda: Customer(address=123, **base_kwargs), "Customer com address=int (ERRO esperado)")
    teste_construtor(lambda: Customer(address="Rua", **base_kwargs), "Customer com address=str (ERRO esperado)")
    teste_construtor(lambda: Customer(address=object(), **base_kwargs), "Customer com address=object (ERRO esperado)")
    teste_construtor(lambda: Customer(address=None, **base_kwargs), "Customer com address=None (ERRO esperado)")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items() if k != 'address'}), "Customer sem address (ERRO esperado)")
    print("\n")

    # testes negativos - register_day
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        birthday=valid_date, phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(register_day="01-01-2000", **base_kwargs), "Customer com register_day=str inválido (ERRO esperado)")
    teste_construtor(lambda: Customer(register_day="2000-01-01", **base_kwargs), "Customer com register_day=str inválido (mas formato ISO válido) (ERRO esperado)")
    teste_construtor(lambda: Customer(register_day="", **base_kwargs), "Customer com register_day str vazio (ERRO esperado)")
    teste_construtor(lambda: Customer(register_day=object(), **base_kwargs), "Customer com register_day=object (ERRO esperado)")
    print("\n")

    #metodos
    print("\n Testes dos Métodos\n")
    valid_customer_1_order = Customer(
            name="Marie Curie",
            email="marie@bestdoggie.com",
            password_hash="ballie",
            birthday=Date(7, 6, 2018),
            phone="(61)88888-8888",
            address=valid_address,
            id=3,
            register_day=Date(9, 3, 2020)
        )

    dummy_order = Order(
        customer=valid_customer,
        date=Date(1, 1, 2022),
        id=125
    )

    gummy_order = Order(
        customer=valid_customer_min,
        id=250,
        date=Date(2, 2, 1950),
        total=35,
        full_price=55,
        global_discount=20
    )

    valid_customer.orders.extend([Order(customer=valid_customer, id=i) for i in range(1, 6)])
    valid_customer.orders.append(gummy_order)
    valid_customer_1_order.orders.append(dummy_order)
    valid_customer_6_order = valid_customer

    # metodos
    # __str__
    teste_metodo(lambda: str(valid_customer_min), "__str__() com Customer válido com dados mínimos (sem id e sem register_day passado explicitamente) (customer com name='Bob', emai='bobby@email.com', esperado)") 
    print("\n")
    teste_metodo(lambda: str(valid_customer_1_order), "__str__() com Customer válido com dados completos (com id e com register_day passado explicitamente) e atributo-lista orders com 1 order (customer com name='Marie Curie', emai='marie@bestdoggie.com', esperado)")
    print("\n")
    teste_metodo(lambda: str(valid_customer_6_order), "__str__() com Customer válido com dados completos (com id e com register_day passado explicitamente) e atributo-lista orders com 6 orders (customer com name='Donna Madonna', e-mai='donnadodona@email.com', esperado)")
    print("\n")
    
    # __eq__
    customer = valid_customer
    customer_igual = valid_customer
    customer_diferente = Customer(name="Bruno", email="bruno@neuro.com", password_hash="cerebelo", birthday=Date(14, 1, 1994), phone="6197777-7777", address=valid_address)
    customer_sem_id = valid_customer_min

    teste_metodo(lambda: customer == customer_igual, "__eq__() com id igual (True esperado)")
    teste_metodo(lambda: customer == customer_diferente, "__eq__() com id diferente (False esperado)")
    teste_metodo(lambda: customer == customer_sem_id, "__eq__() com um Customer sem id (False esperado)")
    teste_metodo(lambda: customer == 'string', "__eq__() Customer X string (False esperado)")
    teste_metodo(lambda: customer == object(), "__eq__() Customer X Object (False esperado)")
    teste_metodo(lambda: customer == None, "__eq__() Customer X None (False esperado)")
    print("\n")

    # get_order_history() (positivos)
    teste_metodo(lambda: valid_customer_1_order.get_order_history(), "get_order_history() com customer válido cujo atributo-lista orders tem 1 order (OK esperado)")
    teste_metodo(lambda: valid_customer_6_order.get_order_history(), "get_order_history() com customer válido cujo atributo-lista orders tem 6 orders (OK esperado)")

    # get_order_history() (negativos)
    teste_metodo(lambda: valid_customer_min.get_order_history(), "get_order_history() com customer válido cujo atributo-lista orders está vazia (OK esperado)")
    print("\n")

    # get_last_order() (positivos)
    teste_metodo(lambda: valid_customer_1_order.get_last_order(), "get_last_order() com customer válido cujo atributo-lista orders tem 1 order (order com id=125 esperada)")
    teste_metodo(lambda: valid_customer_6_order.get_last_order(), "get_last_order() com customer válido cujo atributo-lista orders tem 6 orders (order com id=250 esperada)")

    # get_last_order() (negativos)
    teste_metodo(lambda: valid_customer_min.get_last_order(), "get_last_order() com customer válido cujo atributo-lista orders está vazia (ERRO esperado)")
    print("\n")

    # add_order() (positivos)
    bummy_order = Order(
        customer=valid_customer_min,
        full_price=0,
        id=500,
        date=Date(3, 3, 1925),
        global_discount=0,
        total=0
    )
    yummy_order = Order(
        customer=valid_customer_6_order,
        full_price=0,
        id=750,
        date=Date(3, 3, 1925),
        global_discount=0,
        total=0
    )
    teste_metodo(lambda: valid_customer_min.add_order(bummy_order), "add_order() com customer válido cujo atributo-lista orders está vazia (OK esperado)")
    teste_metodo(lambda: valid_customer_min.get_last_order(), "get_last_order() após adicionar 1 order ao atributo-lista orders vazia de customer válido (order com id=500 esperado)")
    teste_metodo(lambda: valid_customer_6_order.add_order(yummy_order), "add_order() com customer válido cujo atributo-lista orders tem 7 orders (OK esperado)")   
    teste_metodo(lambda: valid_customer_6_order.get_last_order(), "get_last_order() após adicionar 1 order ao atributo-lista orders com 7 orders de customer válido (order com id=750 esperado)")

    # add_order() (negativos)
    teste_metodo(lambda: valid_customer.add_order("não é order"), "add_order() com tipo inválido string (ERRO esperado)")
    teste_metodo(lambda: valid_customer.add_order(123), "add_order() com tipo inválido int (ERRO esperado)")
    teste_metodo(lambda: valid_customer.add_order(object), "add_order() com tipo inválido objeto Object (ERRO esperado)")
    teste_metodo(lambda: valid_customer.add_order(None), "add_order() com tipo inválido None (ERRO esperado)")
    teste_metodo(lambda: valid_customer.add_order(), "add_order() sem argumento (ERRO esperado)")
    teste_metodo(lambda: valid_customer.add_order(bummy_order), "add_order com order válida, mas inconsistente (de outro Customer) (ERRO esperado)")
    print("\n")

    # validate_customer() (positivos)
    teste_metodo(lambda: Customer.validate_customer(valid_customer_1_order), "validate_customer() com objeto Customer válido com dados completos (com id e com register_day passado explicitamente) e com atributo-lista orders com 1 único elemento (OK esperado)")
    teste_metodo(lambda: Customer.validate_customer(valid_customer_min), "validate_customer() com objeto Customer válido com dados mínimos (sem id e sem register_day passado explicitamente) e com atributo-lista orders vazia (OK esperado)")
    teste_metodo(lambda: Customer.validate_customer(valid_customer_6_order), "validate_customer() com objeto Customer válido com dados completos (com id, com register_day passado explicitamente) e com atributo-lista orders populada com mais de 1 elemento (OK esperado)")

    # validate_customer() (negativos)
    teste_metodo(lambda: Customer.validate_customer("string"), "validate_customer() com tipo inválido string (ERRO esperado)")
    teste_metodo(lambda: Customer.validate_customer(123), "validate_customer() com tipo inválido int (ERRO esperado)")
    teste_metodo(lambda: Customer.validate_customer(object), "validate_customer() com tipo inválido objeto Object (ERRO esperado)")
    teste_metodo(lambda: Customer.validate_customer(None), "validate_customer() com tipo inválido None (ERRO esperado)")
    teste_metodo(lambda: Customer.validate_customer(), "validate_customer() sem argumento (ERRO esperado)")
    print("\n")
