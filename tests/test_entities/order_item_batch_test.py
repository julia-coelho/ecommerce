#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo


def test_order_item_batch():
    """teste da classe-entidade OrderItemBatch"""

    from entities import Date, Category, Product
    from entities.address import Address
    from entities.customer import Customer
    from entities.order import Order
    from entities.order_item import OrderItem
    from entities.product_batch import ProductBatch
    from entities.order_item_batch import OrderItemBatch

    print("\n=================================")
    print(" Testes da classe OrderItemBatch ")
    print("=================================\n")

    # objetos auxiliares
    cat = Category(name="Remédios", id=1)
    prod = Product(name="Paracetamol", brand="NeoQuímica", category=cat, unit_price=20.0, id=101)
    hoje = Date.today()
    venc = Date(1, 1, 2026)
    batch = ProductBatch(product=prod, batch_number="LOTEA1", manufacturing_date=hoje, due_date=venc, quantity=50, id=11)

    end = Address("70000-000", "DF", "Brasília", "Asa Norte", "Rua A", "10")
    cliente = Customer("Paciente Zero", "paz@email.com", "hash123", Date(1,1,1990), "61999999999", end, id=1)
    pedido = Order(customer=cliente, id=1000)

    # item relacionado ao batch e ao pedido
    item = OrderItem(product=prod, order=pedido, quantity=0)

    #construtor
    print("\n Testes do Construtor\n")

    # teste positivo do construtor
    valid_oib_min = teste_construtor(
        lambda: OrderItemBatch(product_batch=batch, order_item=item, quantity=5),
        "OrderItemBatch válido com dados mínimos (sem id) (OK esperado)"
    )

    valid_oib = teste_construtor(
        lambda: OrderItemBatch(product_batch=batch, order_item=item, quantity=2, id=10),
        "OrderItemBatch válido com dados completos (com id) (OK esperado)"
    )
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    base_kwargs = dict(product_batch=batch, order_item=item, quantity=5)
    teste_construtor(lambda: OrderItemBatch(id="um", **base_kwargs), "OrderItemBatch com id=str (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(id=0, **base_kwargs), "OrderItemBatch com id=0 (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(id=-1, **base_kwargs), "OrderItemBatch com id negativo (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(id=3.14, **base_kwargs), "OrderItemBatch com id=float (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(id=object(), **base_kwargs), "OrderItemBatch com id=object (ERRO esperado)")
    print("\n")

    # testes negativos - product_batch
    base_kwargs = dict(order_item=item, quantity=5)
    teste_construtor(lambda: OrderItemBatch(product_batch="string", **base_kwargs), "OrderItemBatch com product_batch=str (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(product_batch=123, **base_kwargs), "OrderItemBatch com product_batch=int (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(product_batch=object(), **base_kwargs), "OrderItemBatch com product_batch=object (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(product_batch=None, **base_kwargs), "OrderItemBatch com product_batch=None (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(order_item=item, quantity=5), "OrderItemBatch sem product_batch (ERRO esperado)")
    print("\n")

    # testes negativos - order_item
    base_kwargs = dict(product_batch=batch, quantity=5)
    teste_construtor(lambda: OrderItemBatch(order_item="item", **base_kwargs), "OrderItemBatch com order_item=str (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(order_item=123, **base_kwargs), "OrderItemBatch com order_item=int (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(order_item=object(), **base_kwargs), "OrderItemBatch com order_item=object (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(order_item=None, **base_kwargs), "OrderItemBatch com order_item=None (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(product_batch=batch, quantity=5), "OrderItemBatch sem order_item (ERRO esperado)")
    print("\n")

    # testes negativos - quantity
    base_kwargs = dict(product_batch=batch, order_item=item)
    teste_construtor(lambda: OrderItemBatch(quantity="5", **base_kwargs), "OrderItemBatch com quantity=str (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(quantity=-2, **base_kwargs), "OrderItemBatch com quantity negativo (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(quantity=3.5, **base_kwargs), "OrderItemBatch com quantity=float (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(quantity=object(), **base_kwargs), "OrderItemBatch com quantity=object (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(quantity=None, **base_kwargs), "OrderItemBatch com quantity=None (ERRO esperado)")
    teste_construtor(lambda: OrderItemBatch(product_batch=batch, order_item=item), "OrderItemBatch sem quantity (ERRO esperado)")
    prod_outro = Product(name="Ibuprofeno", brand="Medley", category=cat, unit_price=25.0, id=202)
    batch_errado = ProductBatch(product=prod_outro, batch_number="LOTEB1", manufacturing_date=hoje, quantity=100)
    teste_construtor(lambda: OrderItemBatch(product_batch=batch_errado, order_item=item, quantity=5), "OrderItemBatch com produto do batch diferente do produto do item (ERRO esperado)")
    print("\n")

    #metodos
    print("\n Testes dos Métodos\n")
    if valid_oib and valid_oib_min:
        # __str__
        teste_metodo(lambda: str(valid_oib_min), "__str__() com OrderItemBatch válido com dados mínimos (sem id) (orderitembatch com product='Paracetamol', brand='NeoQuímica', product_batch='LOTEA1', quantidade=5 esperado)")
        teste_metodo(lambda: str(valid_oib), "__str__() com OrderItemBatch válido com dados mínimos (sem id) (orderitembatch com product='Paracetamol', brand='NeoQuímica', product_batch='LOTEA1', quantidade=2 esperado)")
        print("\n")

        # __eq__
        oib_igual = OrderItemBatch(product_batch=batch, order_item=item, quantity=5, id=1)
        oib_diferente = OrderItemBatch(product_batch=batch, order_item=item, quantity=5, id=2)
        oib_sem_id = OrderItemBatch(product_batch=batch, order_item=item, quantity=5)
        teste_metodo(lambda: oib_igual == OrderItemBatch(product_batch=batch, order_item=item, quantity=5, id=1), "__eq__() com id igual (True esperado)")
        teste_metodo(lambda: oib_igual == oib_diferente, "__eq__() com id diferente (False esperado)")
        teste_metodo(lambda: oib_igual == oib_sem_id, "__eq__() com um OrderItemBatch sem id (False esperado)")
        teste_metodo(lambda: oib_igual == 'string', "__eq__() OrderItemBatch X string (False esperado)")
        teste_metodo(lambda: oib_igual == object(), "__eq__() OrderItemBatch X Object (False esperado)")
        teste_metodo(lambda: oib_igual == None, "__eq__() OrderItemBatch X None (False esperado)")

        print("\n")

        # is_from_expired_batch()
        expired_batch = ProductBatch(product=prod, batch_number="EXP00", manufacturing_date=Date(1, 1, 1900), quantity=25, due_date=Date(1, 1, 1950))
        valid_expired_oib = OrderItemBatch(product_batch=expired_batch, order_item=item, quantity=3)
        teste_metodo(lambda: valid_oib.is_from_expired_batch(), "is_from_expired_batch() de OrderItemBatch válido cujo ProductBatch não está expirado (False esperado)")
        teste_metodo(lambda: valid_expired_oib.is_from_expired_batch(), "is_from_expired_batch() com OrderItemBatch válido cujo ProductBatch está expirado (True esperado)")
        print("\n")

        # get_product_name_and_brand()
        teste_metodo(lambda: valid_oib.get_product_name_and_brand(), "get_product_name_and_brand() de OrderItemBatch válido ('Paracetamol' e 'NeoQuímica' esperados)")
        print("\n")

        # validate_order_item_batch() (positivos)
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch(valid_oib_min), "validate_order_item_batch() com objeto OrderItemBatch válido com dados mínimos (sem id) (OK esperado)")
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch(valid_oib), "validate_order_item_batch() com objeto OrderItemBatch válido com id (OK esperado)")

        # validate_order_item_batch() (negativos)
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch('string'), "validate_order_item_batch() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch(123), "validate_order_item_batch() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch(object()), "validate_order_item_batch() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch(None), "validate_order_item_batch() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: OrderItemBatch.validate_order_item_batch(), "validate_order_item_batch() sem argumento (ERRO esperado)")
        print("\n")
