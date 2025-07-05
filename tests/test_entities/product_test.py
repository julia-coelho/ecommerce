# Aluna: Júlia Coelho Rodrigues
# RA: 22408388

from tests import teste_construtor, teste_metodo

def test_product():
    """teste da classe-entidade Product"""

    from entities import Product
    from entities import Category

    print("\n==========================")
    print(" Testes da classe Product ")
    print("==========================\n")

    # objetos auxiliares
    categoria = Category(name="Medicamentos", id=1)

    # construtor
    print("\n Testes do Construtor\n")

    # testes positivos
    prod_min = teste_construtor(lambda: Product(name="Dipirona", brand="Medley", category=categoria, unit_price=10.0), "Product válido com dados mínimos (sem id e sem unit_discount passado explicitamente) (OK esperado)")
    prod_completo = teste_construtor(lambda: Product(name="Paracetamol", brand="NeoQuímica", category=categoria, unit_price=20.0, unit_discount=5.0, id=1), "Product válido com dados completos (com id e com uunit_discount passado explicitamente) (OK esperado)")
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    base_kwargs = dict(name="Produto", brand="Marca", category=categoria, unit_price=10.0)
    teste_construtor(lambda: Product(id="um", **base_kwargs), "Product com id=str (ERRO esperado)")
    teste_construtor(lambda: Product(id=0, **base_kwargs), "Product com id=0 (ERRO esperado)")
    teste_construtor(lambda: Product(id=-1, **base_kwargs), "Product com id negativo (ERRO esperado)")
    teste_construtor(lambda: Product(id=3.14, **base_kwargs), "Product com id=float (ERRO esperado)")
    teste_construtor(lambda: Product(id=object(), **base_kwargs), "Product com id=object (ERRO esperado)")
    print("\n")

    # testes negativos - name
    base_kwargs = dict(brand="Marca", category=categoria, unit_price=10.0)
    teste_construtor(lambda: Product(name="", **base_kwargs), "Product com name vazio (ERRO esperado)")
    teste_construtor(lambda: Product(name=123, **base_kwargs), "Product com name=int (ERRO esperado)")
    teste_construtor(lambda: Product(name=object(), **base_kwargs), "Product com name=object (ERRO esperado)")
    teste_construtor(lambda: Product(name=None, **base_kwargs), "Product com name=None (ERRO esperado)")
    teste_construtor(lambda: Product(**{k: v for k, v in base_kwargs.items()}), "Product sem name (ERRO esperado)")
    print("\n")

    # testes negativos - brand
    base_kwargs = dict(name="Produto", category=categoria, unit_price=10.0)
    teste_construtor(lambda: Product(brand="", **base_kwargs), "Product com brand vazio (ERRO esperado)")
    teste_construtor(lambda: Product(brand=123, **base_kwargs), "Product com brand=int (ERRO esperado)")
    teste_construtor(lambda: Product(brand=object(), **base_kwargs), "Product com brand=object (ERRO esperado)")
    teste_construtor(lambda: Product(brand=None, **base_kwargs), "Product com brand=None (ERRO esperado)")
    teste_construtor(lambda: Product(**{k: v for k, v in base_kwargs.items()}), "Product sem brand (ERRO esperado)")
    print("\n")

    # testes negativos - category
    base_kwargs = dict(name="Produto", brand="Marca", unit_price=10.0)
    teste_construtor(lambda: Product(category="categoria", **base_kwargs), "Product com category=str (ERRO esperado)")
    teste_construtor(lambda: Product(category=object(), **base_kwargs), "Product com category=object (ERRO esperado)")
    teste_construtor(lambda: Product(category=None, **base_kwargs), "Product com category=None (ERRO esperado)")
    teste_construtor(lambda: Product(**{k: v for k, v in base_kwargs.items()}), "Product sem category (ERRO esperado)")
    print("\n")

    # testes negativos - unit_price
    base_kwargs = dict(name="Produto", brand="Marca", category=categoria)
    teste_construtor(lambda: Product(unit_price=-10.0, **base_kwargs), "Product com unit_price negativo (ERRO esperado)")
    teste_construtor(lambda: Product(unit_price="10.0", **base_kwargs), "Product com unit_price=str (ERRO esperado)")
    teste_construtor(lambda: Product(unit_price=object(), **base_kwargs), "Product com unit_price=object (ERRO esperado)")
    teste_construtor(lambda: Product(unit_price=None, **base_kwargs), "Product com unit_price=None (ERRO esperado)")
    teste_construtor(lambda: Product(**{k: v for k, v in base_kwargs.items()}), "Product sem unit_price (ERRO esperado)")
    print("\n")

    # testes negativos - unit_discount (atributo opcional)
    base_kwargs = dict(name="Produto", brand="Marca", category=categoria, unit_price=10.0)
    teste_construtor(lambda: Product(unit_discount="5", **base_kwargs), "Product com unit_discount=str (ERRO esperado)")
    teste_construtor(lambda: Product(unit_discount=-5.0, **base_kwargs), "Product com unit_discount negativo (ERRO esperado)")
    teste_construtor(lambda: Product(unit_discount=object(), **base_kwargs), "Product com unit_discount=object (ERRO esperado)")
    teste_construtor(lambda: Product(name="Produto", brand="Marca", category=categoria, unit_price=5.0, unit_discount=10.0), "Product com unit_discount > unit_price (ERRO esperado)")
    print("\n")


    # metodos
    print("\n Testes dos Métodos\n")
    if prod_min and prod_completo:
        # __str__
        teste_metodo(lambda: str(prod_min), "__str__() de Product válido com dados mínimos (sem id e sem unit_discount) (product com name='Dipirona' e brand='Medley' esperado)")
        teste_metodo(lambda: str(prod_completo), "__str__() de Product válido com dados completos (com id e com unit_discount) (product com name='Paracetamol' e brand='NeoQuímica' esperado)")
        print("\n")

        # __eq__
        igual = Product(name="Paracetamol", brand="NeoQuímica", category=categoria, unit_price=20.0, unit_discount=5.0, id=1)
        diferente = Product(name="Dipirona", brand="Novalgina", category=categoria, unit_price=5.0, id=2)
        sem_id = Product(name="Paracetamol", brand="NeoQuímica", category=categoria, unit_price=20.0, unit_discount=5.0)

        teste_metodo(lambda: prod_completo == igual, "__eq__() com id igual (True esperado)")
        teste_metodo(lambda: prod_completo == diferente, "__eq__() com id diferente (False esperado)")
        teste_metodo(lambda: prod_completo == sem_id, "__eq__() com um Product sem id (False esperado)")
        teste_metodo(lambda: prod_completo == "string", "__eq__() Product X string (False esperado)")
        teste_metodo(lambda: prod_completo == object(), "__eq__() Product X Object (False esperado)")
        teste_metodo(lambda: prod_completo == None, "__eq__() Product X None (False esperado)")
        print("\n")

        # get_formatted_unit_price()
        teste_metodo(lambda: prod_min.get_formatted_unit_price(), "get_formatted_unit_price() de Product válido com dados mínimos (sem id e sem unit_discount) ('R$ 10.00' esperado)")
        teste_metodo(lambda: prod_completo.get_formatted_unit_price(), "get_formatted_unit_price() de Product válido com dados completos (com id e com unit_discount) ('R$ 20.00' esperado)")
        print("\n")

        # get_formatted_unit_discount()
        teste_metodo(lambda: prod_min.get_formatted_unit_discount(), "get_formatted_unit_discount() de Product válido com dados mínimos (sem id e sem unit_discount) ('R$ 0.00' esperado)")
        print("\n")
        teste_metodo(lambda: prod_completo.get_formatted_unit_discount(), "get_formatted_unit_discount() de Product válido com dados completos (com id e com unit_discount) ('R$ 5.00' esperado)")
        print("\n")

        # final_unit_price (property)
        teste_metodo(lambda: prod_min.final_unit_price, "final_unit_price de produto sem desconto (property, '10.0' esperado)")
        teste_metodo(lambda: prod_completo.final_unit_price, "final_unit_price de produto com desconto (property, '15.0' esperado)")
        print("\n")

        # get_formatted_final_unit_price()
        teste_metodo(lambda: prod_min.get_formatted_final_unit_price(), "get_formatted_final_price() de Product válido com dados mínimos (sem id e sem unit_discount) ('R$ 10.00' esperado)")
        teste_metodo(lambda: prod_completo.get_formatted_final_unit_price(), "get_formatted_final_price() de Product válido com dados completos (com id e com unit_discount) ('R$ 15.00' esperado)")
        print("\n")

        # matches_keyword
        teste_metodo(lambda: prod_completo.matches_keyword("paracetamol"), "matches_keyword() com keyword igual ao nome (True esperado)")
        teste_metodo(lambda: prod_completo.matches_keyword("neoquímica"), "matches_keyword() com keyword igual à marca (True esperado)")
        teste_metodo(lambda: prod_completo.matches_keyword("medicamentos"), "matches_keyword() com keyword igual à categoria (True esperado)")
        teste_metodo(lambda: prod_completo.matches_keyword("ibuprofeno"), "matches_keyword() com keyword que não aparece em nenhum campo (False esperado)")
        print("\n")

        # matches_category() (positivos)
        outra_cat = Category(name="Cosméticos", id=2)
        teste_metodo(lambda: prod_completo.matches_category(categoria), "matches_category() com categoria igual (True esperado)")
        teste_metodo(lambda: prod_completo.matches_category(outra_cat), "matches_category() com categoria diferente (False esperado)")

        # matches_category() (negativos)
        teste_metodo(lambda: prod_completo.matches_category("categoria"), "matches_category() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: prod_completo.matches_category(123), "matches_category() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: prod_completo.matches_category(object()), "matches_category() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: prod_completo.matches_category(None), "matches_category() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: prod_completo.matches_category(), "matches_category() sem argumento (ERRO esperado)")
        print("\n")

        # validate_product() (positivos)
        teste_metodo(lambda: Product.validate_product(prod_min), "validate_product() com objeto Product válido com dados mínimos (sem id e sem unit_discount passado explicitamente) (OK esperado)")
        teste_metodo(lambda: Product.validate_product(prod_completo), "validate_product() com objeto Product válido com dados completos (com id e com unit_discount passado explicitamente) (OK esperado)")

        # validate_product() (negativos)
        teste_metodo(lambda: Product.validate_product("produto"), "validate_product() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: Product.validate_product(123), "validate_product() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: Product.validate_product(object()), "validate_product() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: Product.validate_product(None), "validate_product() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: Product.validate_product(), "validate_product() sem argumento (ERRO esperado)")
        print("\n")
