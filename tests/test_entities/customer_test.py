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
    print("\n========================")
    print("Testes da classe Customer")
    print("========================\n")

    # objetos auxiliares
    valid_date = Date(1, 1, 2000)
    valid_address = Address("12345-678", "SP", "São Paulo", "Centro", "Rua A", "123")
    valid_register_day = Date(2, 2, 2020)

    #construtor
    print("\n Testes do Construtor")

    # teste positivo do construtor
    valid_customer = teste_construtor(
        lambda: Customer(
            name="João",
            email="joao@email.com",
            password_hash="senhaSegura123",
            birthday=valid_date,
            phone="11999999999",
            address=valid_address,
            id=1,
            register_day=valid_register_day
        ),
        "Customer válido com dados completos"
    )

    # teste positivo sem id e register_day
    valid_customer_min = teste_construtor(
        lambda: Customer(
            name="Maria",
            email="maria@email.com",
            password_hash="outraSenhaSegura",
            birthday=valid_date,
            phone="(21)98888-7777",
            address=valid_address
        ),
        "Customer válido com dados mínimos"
    )
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos para name
    base_kwargs = dict(
        email="teste@email.com", password_hash="senha", birthday=valid_date,
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(name=None, **base_kwargs), "Customer com name=None")
    teste_construtor(lambda: Customer(name=123, **base_kwargs), "Customer com name=int")
    teste_construtor(lambda: Customer(name=3.14, **base_kwargs), "Customer com name=float")
    teste_construtor(lambda: Customer(name=object(), **base_kwargs), "Customer com name=object")
    teste_construtor(lambda: Customer(name="", **base_kwargs), "Customer com name vazio")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem name")
    print("\n")

    # testes negativos para email
    base_kwargs = dict(
        name="Joao", password_hash="senha", birthday=valid_date,
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(email=None, **base_kwargs), "Customer com email=None")
    teste_construtor(lambda: Customer(email="sem_arroba.com", **base_kwargs), "Customer com email malformado")
    teste_construtor(lambda: Customer(email="sem_extensao@a.", **base_kwargs), "Customer com email malformado")
    teste_construtor(lambda: Customer(email="sem_extensao@a", **base_kwargs), "Customer com email malformado")
    teste_construtor(lambda: Customer(email="", **base_kwargs), "Customer com email vazio")
    teste_construtor(lambda: Customer(email=123, **base_kwargs), "Customer com email=int")
    teste_construtor(lambda: Customer(email=12.3, **base_kwargs), "Customer com email=float")
    teste_construtor(lambda: Customer(email=object(), **base_kwargs), "Customer com email=object")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem email")
    print("\n")

    # testes negativos para password_hash
    base_kwargs = dict(
        name="Joao", email="teste@email.com", birthday=valid_date,
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(password_hash=None, **base_kwargs), "Customer com password_hash=None")
    teste_construtor(lambda: Customer(password_hash="", **base_kwargs), "Customer com password_hash vazio")
    teste_construtor(lambda: Customer(password_hash=123, **base_kwargs), "Customer com password_hash=int")
    teste_construtor(lambda: Customer(password_hash=12.3, **base_kwargs), "Customer com password_hash=float")
    teste_construtor(lambda: Customer(password_hash=object(), **base_kwargs), "Customer com password_hash=object")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem password_hash")
    print("\n")

    # testes negativos para birthday
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        phone="11999999999", address=valid_address
    )
    teste_construtor(lambda: Customer(birthday=None, **base_kwargs), "Customer com birthday=None")
    teste_construtor(lambda: Customer(birthday="01-01-2000", **base_kwargs), "Customer com birthday=str inválido")
    teste_construtor(lambda: Customer(birthday="2000-01-01", **base_kwargs), "Customer com birthday=str inválido (mas formato ISO válido)")
    teste_construtor(lambda: Customer(birthday="", **base_kwargs), "Customer com birthday str vazio")
    teste_construtor(lambda: Customer(birthday=object(), **base_kwargs), "Customer com birthday=object")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items()}), "Customer sem birthday")
    print("\n")

    # testes negativos para phone
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        birthday=valid_date, address=valid_address
    )
    teste_construtor(lambda: Customer(phone=123, **base_kwargs), "Customer com phone=int")
    teste_construtor(lambda: Customer(phone=3.14, **base_kwargs), "Customer com phone=float")
    teste_construtor(lambda: Customer(phone="abcdefghijk", **base_kwargs), "Customer com phone com letras")
    teste_construtor(lambda: Customer(phone="(61) 9999-999", **base_kwargs), "Customer com phone com poucos dígitos")
    teste_construtor(lambda: Customer(phone="619999999999", **base_kwargs), "Customer com phone com dígitos demais")
    teste_construtor(lambda: Customer(phone=None, **base_kwargs), "Customer com phone=None")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items() if k != 'phone'}), "Customer sem phone")
    print("\n")

    # testes negativos para address
    base_kwargs = dict(
        name="Joao", email="teste@email.com", password_hash="senha",
        birthday=valid_date, phone="11999999999"
    )
    teste_construtor(lambda: Customer(address=123, **base_kwargs), "Customer com address=int")
    teste_construtor(lambda: Customer(address="Rua", **base_kwargs), "Customer com address=str")
    teste_construtor(lambda: Customer(address=object(), **base_kwargs), "Customer com address=object")
    teste_construtor(lambda: Customer(address=None, **base_kwargs), "Customer com address=None")
    teste_construtor(lambda: Customer(**{k: v for k, v in base_kwargs.items() if k != 'address'}), "Customer sem address")
    print("\n")

    #metodos
    print("\n Testes dos Métodos\n")
    valid_customer_1_order = Customer(
            name="Marie Curie",
            email="marie@bestdoggie.com",
            password_hash="ballie",
            birthday=Date(7, 6, 2007),
            phone="(61)88888-8888",
            address=valid_address
        )

    dummy_order = Order(
        customer=valid_customer,
        date=Date(1, 1, 2022),
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
    teste_metodo(lambda: str(valid_customer_min), "__str__()") 
    print("\n")
    teste_metodo(lambda: str(valid_customer_1_order), "__str__()")
    print("\n")
    teste_metodo(lambda: str(valid_customer_6_order), "__str__()")
    print("\n")
    
    # __eq__
    customer = valid_customer
    customer_igual = valid_customer
    customer_diferente = Customer(name="Bruno", email="bruno@neuro.com", password_hash="cerebelo", birthday=Date(14, 1, 1994), phone="6197777-7777", address=valid_address)
    customer_sem_id = valid_customer_min

    teste_metodo(lambda: customer == customer_igual, "__eq__() com id igual")
    teste_metodo(lambda: customer == customer_diferente, "__eq__() com id diferente")
    teste_metodo(lambda: customer == customer_sem_id, "__eq__() com um Customer sem id")
    teste_metodo(lambda: customer == 'string', "__eq__() Customer X string")
    teste_metodo(lambda: customer == object(), "__eq__() Customer X Object")
    teste_metodo(lambda: customer == None, "__eq__() Customer X None")
    print("\n")

    # get_order_history() (positivos)
    teste_metodo(lambda: valid_customer_1_order.get_order_history(), "get_order_history() com lista com 1 order")
    teste_metodo(lambda: valid_customer_6_order.get_order_history(), "get_order_history() com lista com 6 orders")

    # get_order_history() (negativos)
    teste_metodo(lambda: valid_customer_min.get_order_history(), "get_order_history() com lista vazia")
    print("\n")

    # get_last_order() (positivos)
    teste_metodo(lambda: valid_customer_1_order.get_last_order(), "get_last_order() com lista com 1 order")
    teste_metodo(lambda: valid_customer_6_order.get_last_order(), "get_last_order() com lista com 6 orders - verificar se pegou a order correta: id=250")

    # get_last_order() (negativos)
    teste_metodo(lambda: valid_customer_min.get_last_order(), "get_last_order() com lista vazia")
    print("\n")

    # add_order() (positivo)
    bummy_order = Order(
        customer=valid_customer_min,
        full_price=0,
        id=500,
        date=Date(3, 3, 1925),
        global_discount=0,
        total=0
    )
    teste_metodo(lambda: valid_customer_min.add_order(bummy_order), "add_order() com objeto válido - em lista vazia")
    teste_metodo(lambda: valid_customer_min.get_last_order(), "get_last_order() após adicionar 1 order em lista vazia (a order obtida tem id=500)")
    teste_metodo(lambda: valid_customer_6_order.add_order(bummy_order), "add_order() com objeto válido - em lista de 7 orders")   
    teste_metodo(lambda: valid_customer_6_order.get_last_order(), "get_last_order() após adicionar 1 order em lista de 7 orders (verificar se a order obtida tem id=500)")

    # add_order() (negativos)
    teste_metodo(lambda: valid_customer.add_order("não é order"), "add_order() com tipo inválido string")
    teste_metodo(lambda: valid_customer.add_order(123), "add_order() com tipo inválido int")
    teste_metodo(lambda: valid_customer.add_order(object), "add_order() com tipo inválido objeto Object")
    teste_metodo(lambda: valid_customer.add_order(None), "add_order() com tipo inválido None")
    teste_metodo(lambda: valid_customer.add_order(), "add_order() sem argumento")
    teste_metodo(lambda: valid_customer.add_order(bummy_order), "add_order com order válida, mas inconsistente (de outro Customer)")
    print("\n")

    # validate_customer() (positivo)
    teste_metodo(lambda: Customer.validate_customer(valid_customer_1_order), "validate_customer() com objeto Customer válido com dados completos (com id, com register_day e com atributo-lista orders com 1 único elemento)")
    teste_metodo(lambda: Customer.validate_customer(valid_customer_min), "validate_customer() com objeto Customer válido com dados mínimos (sem id, sem register_day, com atributo-lista orders vazia")
    teste_metodo(lambda: Customer.validate_customer(valid_customer_6_order), "validate_customer() com objeto Customer válido com dados completos (com id, com register_day e com atributo-lista orders populada com mais de 1 elemento)")

    # validate_customer() (negativo)
    teste_metodo(lambda: Customer.validate_customer("string"), "validate_customer() com tipo inválido string")
    teste_metodo(lambda: Customer.validate_customer(123), "validate_customer() com tipo inválido int")
    teste_metodo(lambda: Customer.validate_customer(object), "validate_customer() com tipo inválido objeto Object")
    teste_metodo(lambda: Customer.validate_customer(None), "validate_customer() com tipo inválido None")
    teste_metodo(lambda: Customer.validate_customer(), "validate_customer() sem argumento")
    print("\n")
