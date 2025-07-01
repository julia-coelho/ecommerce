#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo

def test_order_item():
    """teste da classe-entidade OrderItem"""

    from entities import Date, Category, Product
    from entities.address import Address
    from entities.customer import Customer
    from entities.order import Order
    from entities.order_item import OrderItem
    from entities.product_batch import ProductBatch
    from entities.order_item_batch import OrderItemBatch

    print("\n========================")
    print("Testes da classe OrderItem")
    print("========================\n")

    #objetos auxiliares
    cat = Category(name="Analgésicos", id=1)
    prod = Product(name="Dipirona", brand="EMS", category=cat, unit_price=10.0, id=101)
    end = Address("70000-000", "DF", "Brasília", "Asa Norte", "Rua A", "10")
    cliente = Customer("Usuário Final", "user@dominio.com", "hash123", Date(1,1,1990), "61999999999", end, id=1)
    pedido = Order(customer=cliente, id=1000)

    #construtor
    print("\n Testes do Construtor\n")

    # testes positivos
    item_min = teste_construtor(lambda: OrderItem(product=prod, order=pedido), "OrderItem válido com dados mínimos (sem id, sem quantity passado explicitamente, sem unit_price passado explicitamente e sem unit_discount passado explicitamente)")
    item_complete = teste_construtor(lambda: OrderItem(product=prod, order=pedido, quantity=3, id=10, unit_price=5, unit_discount=2.5), "OrderItem válido com dados completos (com id, com quantity, com unit_price e com unit_discount)")
    print("\n")

    # testes negativos - product
    base_kwargs = dict(order=pedido, quantity=2)
    teste_construtor(lambda: OrderItem(product="produto", **base_kwargs), "OrderItem com product=str")
    teste_construtor(lambda: OrderItem(product=123, **base_kwargs), "OrderItem com product=int")
    teste_construtor(lambda: OrderItem(product=object(), **base_kwargs), "OrderItem com product=object")
    teste_construtor(lambda: OrderItem(product=None, **base_kwargs), "OrderItem com product=None")
    teste_construtor(lambda: OrderItem(order=pedido, quantity=2), "OrderItem sem product")
    print("\n")

    # testes negativos - order
    base_kwargs = dict(product=prod, quantity=2)
    teste_construtor(lambda: OrderItem(order="pedido", **base_kwargs), "OrderItem com order=str")
    teste_construtor(lambda: OrderItem(order=123, **base_kwargs), "OrderItem com order=int")
    teste_construtor(lambda: OrderItem(order=object(), **base_kwargs), "OrderItem com order=object")
    teste_construtor(lambda: OrderItem(order=None, **base_kwargs), "OrderItem com order=None")
    teste_construtor(lambda: OrderItem(product=prod, quantity=2), "OrderItem sem order")
    print("\n")

    # testes negativos - id
    base_kwargs = dict(product=prod, order=pedido, quantity=2)
    teste_construtor(lambda: OrderItem(id=3.5, **base_kwargs), "OrderItem com id=float")
    teste_construtor(lambda: OrderItem(id="3", **base_kwargs), "OrderItem com id=str")
    teste_construtor(lambda: OrderItem(id=-1, **base_kwargs), "OrderItem com id negativo")
    teste_construtor(lambda: OrderItem(id=object(), **base_kwargs), "OrderItem com id=object")
    print("\n")

    # testes negativos - quantity
    base_kwargs = dict(product=prod, order=pedido)
    teste_construtor(lambda: OrderItem(quantity=3.5, **base_kwargs), "OrderItem com quantity=float")
    teste_construtor(lambda: OrderItem(quantity="3", **base_kwargs), "OrderItem com quantity=str")
    teste_construtor(lambda: OrderItem(quantity=-1, **base_kwargs), "OrderItem com quantity negativo")
    teste_construtor(lambda: OrderItem(quantity=object(), **base_kwargs), "OrderItem com quantity=object")
    teste_construtor(lambda: OrderItem(quantity=None, **base_kwargs), "OrderItem com quantity=None")
    teste_construtor(lambda: OrderItem(product=prod, order=pedido), "OrderItem sem quantity")
    print("\n")

    # testes negativos - unit_discount
    base_kwargs = dict(product=prod, order=pedido, quantity=2)
    teste_construtor(lambda: OrderItem(unit_discount="2", **base_kwargs), "OrderItem com unit_discount=str")
    teste_construtor(lambda: OrderItem(unit_discount=-1, **base_kwargs), "OrderItem com unit_discount negativo")
    teste_construtor(lambda: OrderItem(unit_discount=object(), **base_kwargs), "OrderItem com unit_discount=object")
    print("\n")

    #metodos
    print("\n Testes dos Métodos\n")
    if item_min and item_complete:
        # __str__
        teste_metodo(lambda: str(item_min), "__str__() de OrderItem válido com dados mínimos (sem id, sem quantity passado explicitamente, sem unit_price passado explicitamente e sem unit_discount passado explicitamente)")
        teste_metodo(lambda: str(item_complete), "__str__() de OrderItem válido com dados completos (com id, com quantity, com unit_price e com unit_discount)")
        print("\n")

        # __eq__
        item1 = OrderItem(product=prod, order=pedido, quantity=1, id=77)
        item2 = OrderItem(product=prod, order=pedido, quantity=1, id=77)
        item3 = OrderItem(product=prod, order=pedido, quantity=1, id=78)
        item4 = OrderItem(product=prod, order=pedido, quantity=1)
        teste_metodo(lambda: item1 == item2, "__eq__() com id igual")
        teste_metodo(lambda: item1 == item3, "__eq__() com id diferente")
        teste_metodo(lambda: item1 == item4, "__eq__() com um OrderItem sem id")
        teste_metodo(lambda: item1 == 'string', "__eq__() OrderItem X string")
        teste_metodo(lambda: item1 == object(), "__eq__() OrderItem X Object")
        teste_metodo(lambda: item1 == None, "__eq__() OrderItem X None")
        print("\n")

        # add_order_item_batch() (positivo)
        item_complete_starting_empty = OrderItem(product=prod, order=pedido, quantity=0, id=10, unit_price=5, unit_discount=2.5)
        batch1 = ProductBatch(product=prod, batch_number="B1", manufacturing_date=Date(1, 1, 2023), quantity=100, id=1)
        batch2 = ProductBatch(product=prod, batch_number="B2", manufacturing_date=Date(1, 1, 2003), quantity=50, id=2)
        oib1 = OrderItemBatch(product_batch=batch1, order_item=item_complete_starting_empty, quantity=1, id=1)
        oib2 = OrderItemBatch(product_batch=batch2, order_item=item_complete_starting_empty, quantity=2, id=2)
        teste_metodo(lambda: item_complete_starting_empty.add_order_item_batch(oib1), "add_order_item_batch() com batch válido (1ª vez), batch_number='B1' quantity=1")
        teste_metodo(lambda: item_complete_starting_empty.add_order_item_batch(oib1), "add_order_item_batch() com mesmo batch (incrementa quantidade), batch_number='B1' quantity=1")
        teste_metodo(lambda: item_complete_starting_empty.add_order_item_batch(oib2), "add_order_item_batch() com batch válido diferente, mas do mesmo produto (coloca batch no atributo batches de OrderItem, lembrando que batches é uma list[OrderItemBatch]), batch_number='B2' quantity=2")
        print(f"Batches em batches de {item_complete_starting_empty}:")
        for batch in item_complete_starting_empty.batches:
            print(f"{batch}")
        print("\n")

        # add_order_item_batch() (negativo)
        teste_metodo(lambda: item1.add_order_item_batch("batch"), "add_order_item_batch() com tipo inválido string")
        teste_metodo(lambda: item1.add_order_item_batch(123), "add_order_item_batch() com tipo inválido int")        
        teste_metodo(lambda: item1.add_order_item_batch(object()), "add_order_item_batch() com tipo inválido object Object")
        teste_metodo(lambda: item1.add_order_item_batch(None), "add_order_item_batch() com tipo inválido None")
        teste_metodo(lambda: item1.add_order_item_batch(), "add_order_item_batch() sem argumento")
        teste_metodo(lambda: item1.add_order_item_batch(oib2), "add_order_item_batch() com orderitem de batch válido, mas inconsistente para aquele OrderItem específico")
        print("\n")

        # add_order_item_batch_from_db() (positivo)
        item_db = OrderItem(product=prod, order=pedido, quantity=2, id=600, unit_price=25.0, unit_discount=5.00)
        batch_db = ProductBatch(product=prod, batch_number="BDB", manufacturing_date=Date(1,1,2023), quantity=50, id=10)
        oib_db = OrderItemBatch(product_batch=batch_db, order_item=item_db, quantity=2, id=10)
        teste_metodo(lambda: item_db.add_order_item_batch_from_db(oib_db), "add_order_item_batch_from_db() com batch válido")

        # add_order_item_batch_from_db() (negativo)
        item_db2 = OrderItem(product=prod, order=pedido, quantity=2, id=601)
        batch_duplicado = ProductBatch(product=prod, batch_number="REP", manufacturing_date=Date(1,1,2023), quantity=10, id=11)
        oib_dup1 = OrderItemBatch(product_batch=batch_duplicado, order_item=item_db2, quantity=1, id=11)
        oib_dup2 = OrderItemBatch(product_batch=batch_duplicado, order_item=item_db2, quantity=1, id=12)
        item_db2.add_order_item_batch_from_db(oib_dup1)
        teste_metodo(lambda: item1.add_order_item_batch_from_db("batch"), "add_order_item_batch()_from_db com tipo inválido string")
        teste_metodo(lambda: item1.add_order_item_batch_from_db(123), "add_order_item_batch()_from_db com tipo inválido int")        
        teste_metodo(lambda: item1.add_order_item_batch_from_db(object()), "add_order_item_batch()_from_db com tipo inválido object Object")
        teste_metodo(lambda: item1.add_order_item_batch_from_db(None), "add_order_item_batch()_from_db com tipo inválido None")
        teste_metodo(lambda: item1.add_order_item_batch_from_db(), "add_order_item_batch()_from_db sem argumento")
        # soma das quantidades = 3 > 2 (vai dar erro)
        oib_muito = OrderItemBatch(product_batch=batch_db, order_item=item_db2, quantity=3, id=14)
        teste_metodo(lambda: item_db2.add_order_item_batch_from_db(oib_muito), "add_order_item_batch_from_db() excedendo quantity total")
        # duplicado
        teste_metodo(lambda: item_db2.add_order_item_batch_from_db(oib_dup2), "add_order_item_batch_from_db() com batch duplicado")
        # orderitem de orderitembatch errado
        teste_metodo(lambda: item_db2.add_order_item_batch_from_db(oib1), "add_order_item_batch()_from_db com orderitem de batch válido, mas inconsistente (de outro OrderItem)")
        print("\n")

        # propriedades
        item_no_discount = OrderItem(product=prod, order=pedido, id=20, unit_price=10)
        oib3 = OrderItemBatch(product_batch=batch1, order_item=item_no_discount, quantity=1, id=1)
        oib4 = OrderItemBatch(product_batch=batch2, order_item=item_no_discount, quantity=2, id=2)
        item_no_discount.add_order_item_batch(oib3)
        item_no_discount.add_order_item_batch(oib4)
        item_with_discount = OrderItem(product=prod, order=pedido, id=21, unit_price=10, unit_discount=2.5)
        oib5 = OrderItemBatch(product_batch=batch1, order_item=item_with_discount, quantity=1, id=1)
        oib6 = OrderItemBatch(product_batch=batch2, order_item=item_with_discount, quantity=2, id=2)        
        item_with_discount.add_order_item_batch(oib5)
        item_with_discount.add_order_item_batch(oib6)
        teste_metodo(lambda: item_min.final_unit_price, "final_unit_price (unit_price - unit_discount) de OrderItem com lista batches vazia, unit_price=10.0 e unit_discount=0 (propriedade, '10.0' esperado)")
        teste_metodo(lambda: item_no_discount.final_unit_price, "final_unit_price (unit_price - unit_discount) de OrderItem com lista batches populada, unit_price=10.0 e unit_discount=0 (propriedade, '10.0' esperado)")
        teste_metodo(lambda: item_with_discount.final_unit_price, "final_unit_price (unit_price - unit_discount) de OrderItem com lista batches populada, unit_price=10.0 e unit_discount=2.5 (propriedade, '7.5' esperado)")
        print("\n")
        teste_metodo(lambda: item_min.total_price, "total_price (final_price * quantity) de OrderItem com lista batches vazia, quantity=0, unit_price=10.0 e unit_discount=0 (propriedade, '0' ou '0.0' esperado)")
        teste_metodo(lambda: item_no_discount.total_price, "total_price (final_price * quantity) de OrderItem com lista batches populada, quantity=3, unit_price=10.0 e unit_discount=0 (propriedade, '30.0' esperado)")
        teste_metodo(lambda: item_with_discount.total_price, "total_price (final_price * quantity) de OrderItem com lista batches populada, quantity=3, unit_price=10.0 e unit_discount=2.5 (propriedade, '22.5' esperado)")
        print("\n")

        #get_formatted_final_unit_price()
        teste_metodo(lambda: item_with_discount.get_formatted_final_unit_price(), "get_formatted_final_unit_price() de OrderItem com lista batches populada, quantity=3, unit_price=10.0 e unit_discount=2.5 ('R$ 7.50' esperado)")
        print("\n")

        #get_formatted_total_price()
        teste_metodo(lambda: item_with_discount.get_formatted_total_price(), "get_formatted_total_price() de OrderItem com lista batches populada, quantity=3, unit_price=10.0 e unit_discount=2.5 ('R$ 22.50' esperado)")
        print("\n")

        # validate_order_item()
        teste_metodo(lambda: OrderItem.validate_order_item(item_min), "validate_order_item() com objeto OrderItem válido mínimo (sem id, sem due_date e com lista batches vazia)")
        teste_metodo(lambda: OrderItem.validate_order_item(item_complete), "validate_order_item() com objeto OrderItem válido completo (com id, com due_date e lista batches populada)")
        teste_metodo(lambda: OrderItem.validate_order_item('string'), "validate_order_item() com tipo inválido string")
        teste_metodo(lambda: OrderItem.validate_order_item(12), "validate_order_item() com tipo inválido int")
        teste_metodo(lambda: OrderItem.validate_order_item(object()), "validate_order_item() com tipo inválido orbjeto Object")
        teste_metodo(lambda: OrderItem.validate_order_item(None), "validate_order_item() com tipo inválido None")
        teste_metodo(lambda: OrderItem.validate_order_item(), "validate_order_item() sem argumento")
        print("\n")
