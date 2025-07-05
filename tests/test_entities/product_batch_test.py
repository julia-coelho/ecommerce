#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo

def test_product_batch():
    """teste da classe-entidade ProductBatch"""

    from entities import Date, Category, Product
    from entities.product_batch import ProductBatch

    print("\n===============================")
    print(" Testes da classe ProductBatch ")
    print("===============================\n")

    # objetos auxiliares
    cat = Category(name="Remédios", id=1)
    prod = Product(name="Paracetamol", brand="NeoQuímica", category=cat, unit_price=20.0, id=101)
    manuf = Date(1, 1, 2023)
    venc = Date(1, 1, 2026)
    hoje = Date.today()

    # construtor
    print("\n Testes do Construtor\n")

    # testes positivos
    valid_batch_min = teste_construtor(
        lambda: ProductBatch(product=prod, batch_number="LOTEA1", manufacturing_date=manuf, quantity=20),
        "ProductBatch válido com dados mínimos (sem due_date e sem id) (OK esperado)"
    )
    valid_batch_complete = teste_construtor(
        lambda: ProductBatch(product=prod, batch_number="LOTEA1", manufacturing_date=manuf, due_date=venc, quantity=50, id=1),
        "ProductBatch válido com dados completos (com due_date e com id) (OK esperado)"
    )
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    base_kwargs = dict(product=prod, batch_number="LOTE1", manufacturing_date=manuf, due_date=venc, quantity=10)
    teste_construtor(lambda: ProductBatch(id="um", **base_kwargs), "ProductBatch com id=str (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(id=0, **base_kwargs), "ProductBatch com id=0 (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(id=-1, **base_kwargs), "ProductBatch com id negativo (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(id=3.14, **base_kwargs), "ProductBatch com id=float (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(id=object(), **base_kwargs), "ProductBatch com id=object (ERRO esperado)")
    print("\n")

    # testes negativos - product
    base_kwargs = dict(batch_number="LOTE1", manufacturing_date=manuf, due_date=venc, quantity=10)
    teste_construtor(lambda: ProductBatch(product="produto", **base_kwargs), "ProductBatch com product=str (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(product=123, **base_kwargs), "ProductBatch com product=int (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(product=object(), **base_kwargs), "ProductBatch com product=object (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(product=None, **base_kwargs), "ProductBatch com product=None (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(**{k: v for k, v in base_kwargs.items()}), "ProductBatch sem product (ERRO esperado)")
    print("\n")

    # testes negativos - batch_number
    base_kwargs = dict(product=prod, manufacturing_date=manuf, due_date=venc, quantity=10)
    teste_construtor(lambda: ProductBatch(batch_number="", **base_kwargs), "ProductBatch com batch_number vazio (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(batch_number=123, **base_kwargs), "ProductBatch com batch_number=int (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(batch_number=object(), **base_kwargs), "ProductBatch com batch_number=object (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(batch_number=None, **base_kwargs), "ProductBatch com batch_number=None (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(**{k: v for k, v in base_kwargs.items()}), "ProductBatch sem batch_number (ERRO esperado)")
    print("\n")

    # testes negativos - manufacturing_date
    base_kwargs = dict(product=prod, batch_number="LOTE", due_date=venc, quantity=10)
    teste_construtor(lambda: ProductBatch(manufacturing_date="ontem", **base_kwargs), "ProductBatch com manufacturing_date=str (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(manufacturing_date=123, **base_kwargs), "ProductBatch com manufacturing_date=int (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(manufacturing_date=object(), **base_kwargs), "ProductBatch com manufacturing_date=object (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(manufacturing_date=None, **base_kwargs), "ProductBatch com manufacturing_date=None (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(**{k: v for k, v in base_kwargs.items()}), "ProductBatch sem manufacturing_date (ERRO esperado)")
    print("\n")

    # testes negativos - quantity
    base_kwargs = dict(product=prod, batch_number="LOTE", manufacturing_date=manuf, due_date=venc)
    teste_construtor(lambda: ProductBatch(quantity=-5, **base_kwargs), "ProductBatch com quantity negativa (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(quantity="dez", **base_kwargs), "ProductBatch com quantity=str (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(quantity=None, **base_kwargs), "ProductBatch com quantity=None (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(quantity=object(), **base_kwargs), "ProductBatch com quantity=object (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(**{k: v for k, v in base_kwargs.items()}), "ProductBatch sem quantity (ERRO esperado)")
    print("\n")

    # testes negativos - due_date (atributo opcional)
    base_kwargs = dict(product=prod, batch_number="LOTE", manufacturing_date=manuf, quantity=10)
    teste_construtor(lambda: ProductBatch(due_date="2026-01-01", **base_kwargs), "ProductBatch com due_date=str (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(due_date=123, **base_kwargs), "ProductBatch com due_date=int (ERRO esperado)")
    teste_construtor(lambda: ProductBatch(due_date=object(), **base_kwargs), "ProductBatch com due_date=object (ERRO esperado)")
    print("\n")

    # metodos
    print("\n Testes dos Métodos\n")
    if valid_batch_complete and valid_batch_min:
        # __str__
        teste_metodo(lambda: str(valid_batch_min), "__str__() de ProductBatch válido com dados mínimos (sem due_date e sem id) (productbatch com product='Paracetamol', brand='NeoQuímica', product_batch='#LOTEA1', quantity=20 esperado)")
        teste_metodo(lambda: str(valid_batch_complete), "__str__() de ProductBatch válido com dados completos (com due_date e com id) (productbatch com product='Paracetamol', brand='NeoQuímica', product_batch='#LOTEA1', quantity=50 esperado)")
        print("\n")

        # __eq__
        mesmo_id = ProductBatch(product=prod, batch_number="LOTEX", manufacturing_date=manuf, quantity=10, id=1)
        diferente_id = ProductBatch(product=prod, batch_number="LOTEY", manufacturing_date=manuf, quantity=10, id=2)
        sem_id = ProductBatch(product=prod, batch_number="LOTEN", manufacturing_date=manuf, quantity=10)
        teste_metodo(lambda: valid_batch_complete == mesmo_id, "__eq__() com id igual (True esperado)")
        teste_metodo(lambda: valid_batch_complete == diferente_id, "__eq__() com id diferente (False esperado)")
        teste_metodo(lambda: valid_batch_complete == sem_id, "__eq__() com um ProductBatch sem id (False esperado)")
        teste_metodo(lambda: valid_batch_complete == "string", "__eq__() ProductBatch X string (False esperado)")
        teste_metodo(lambda: valid_batch_complete == object(), "__eq__() ProductBatch X Object (False esperado)")
        teste_metodo(lambda: valid_batch_complete == None, "__eq__() ProductBatch X None (False esperado)")
        print("\n")

        # is_expired()
        vencido = ProductBatch(product=prod, batch_number="EXP", manufacturing_date=Date(1,1,1900), due_date=Date(1,1,1950), quantity=10)
        sem_vencimento = ProductBatch(product=prod, batch_number="SEM", manufacturing_date=Date(1,1,2020), quantity=10)
        teste_metodo(lambda: valid_batch_complete.is_expired(), "is_expired() de ProductBatch com lote válido e não vencido (False esperado)")
        teste_metodo(lambda: vencido.is_expired(), "is_expired() de ProductBatch com lote vencido (True esperado)")
        teste_metodo(lambda: sem_vencimento.is_expired(), "is_expired() de ProductBatch sem due_date (False esperado)")
        print("\n")

        # get_product_id()
        teste_metodo(lambda: valid_batch_complete.get_product_id(), "get_product_id() de ProductBatch válido ('101' esperado)")
        print("\n")

        # get_product_name_and_brand()
        teste_metodo(lambda: valid_batch_complete.get_product_name_and_brand(), "get_product_name() de ProductBatch válido ('Paracetamol' e 'NeoQuímica' esperados)")
        print("\n")

        # unit_price (property)
        teste_metodo(lambda: valid_batch_complete.unit_price, "unit_price de ProductBatch válido (property, '20.0' esperado)")
        print("\n")

        # unit_discount (property)
        teste_metodo(lambda: valid_batch_complete.unit_discount, "unit_discount de ProductBatch válido (property, '0.0' esperado)")
        print("\n")

        # final_unit_price (property)
        teste_metodo(lambda: valid_batch_complete.final_unit_price, "final_unit_price de ProductBatch válido (property, '20.0' esperado)")
        print("\n")

        # get_formatted_final_price()
        teste_metodo(lambda: valid_batch_complete.get_formatted_final_price(), "get_formatted_final_price() de ProductBatch válido ('R$ 20.00' esperado)")
        print("\n")

        # days_until_expiration()
        teste_metodo(lambda: valid_batch_complete.days_until_expiration(), "days_until_expiration() de ProductBatch com due_date")
        teste_metodo(lambda: sem_vencimento.days_until_expiration(), "days_until_expiration() de ProductBatch sem due_date (None esperado)")
        teste_metodo(lambda: vencido.days_until_expiration(), "days_until_expiration() de ProductBatch vencido (número negativo esperado)")
        print("\n")

        # validate_product_batch() (positivos)
        teste_metodo(lambda: ProductBatch.validate_product_batch(valid_batch_min), "validate_product_batch() com objeto ProductBatch válido com dados mínimos (sem due_date e sem id) (OK esperado)")
        teste_metodo(lambda: ProductBatch.validate_product_batch(valid_batch_complete), "validate_product_batch() com objeto ProductBatch válido com dados completos (com due_date e com id) (OK esperado)")

        # validate_product_batch() (negativos)
        teste_metodo(lambda: ProductBatch.validate_product_batch("string"), "validate_product_batch() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: ProductBatch.validate_product_batch(123), "validate_product_batch() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: ProductBatch.validate_product_batch(object()), "validate_product_batch() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: ProductBatch.validate_product_batch(None), "validate_product_batch() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: ProductBatch.validate_product_batch(), "validate_product_batch() sem argumento (ERRO esperado)")
        print("\n")
