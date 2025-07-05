#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo


def test_address():
    """teste da classe-entidade Address"""

    from entities import Address

    # testes de Address
    print("\n==========================")
    print(" Testes da classe Address ")
    print("==========================\n")

    # construtor
    print("\n Testes do Construtor\n")

    # testes positivos do construtor
    valid_address_min = teste_construtor(
        lambda: Address(
            cep="12345-678",
            state="SP",
            city="São Paulo",
            district="Centro",
            street="Rua A",
            number="123"
        ),
        "Address válido e com dados mínimos (sem complement) (OK esperado)"
    )

    valid_address_completo = teste_construtor(
        lambda: Address(
            cep="87654-321",
            state="SP",
            city="São Paulo",
            district="Centro",
            street="Rua B",
            number="456",
            complement="Apto 1"
        ),
        "Address válido e com dados completos (com complement) (OK esperado)"
    )
    print("\n\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - cep
    base_kwargs = dict(state="SP", city="São Paulo", district="Centro", street="Rua A", number="123")
    teste_construtor(lambda: Address(cep=12345678, **base_kwargs), "Address com cep=int (ERRO esperado)")
    teste_construtor(lambda: Address(cep=12345.678, **base_kwargs), "Address com cep=float (ERRO esperado)")
    teste_construtor(lambda: Address(cep='A', **base_kwargs), "Address com cep=char (ERRO esperado)")
    teste_construtor(lambda: Address(cep=object(), **base_kwargs), "Address com cep=object (ERRO esperado)")
    teste_construtor(lambda: Address(cep=None, **base_kwargs), "Address com cep=None (ERRO esperado)")
    teste_construtor(lambda: Address(state="SP", city="São Paulo", district="Centro", street="Rua A", number="123"), "Address sem cep (omitido) (ERRO esperado)")
    teste_construtor(lambda: Address(cep="00A00-000", **base_kwargs), "Address com cep com hífen contendo letra maiúscula (00A00-000) (ERRO esperado)")
    teste_construtor(lambda: Address(cep="00000b00", **base_kwargs), "Address com cep sem hífen contendo letra minúscula (00000b00) (ERRO esperado)")
    teste_construtor(lambda: Address(cep="123456789", **base_kwargs), "Address com cep com mais de 8 dígitos (ERRO esperado)")
    teste_construtor(lambda: Address(cep="1234", **base_kwargs), "Address com cep com menos de 8 dígitos (ERRO esperado)")
    teste_construtor(lambda: Address(cep="1234-678", **base_kwargs), "Address com cep com menos de 8 dígitos (ERRO esperado)")
    print("\n")

    # testes negativos - state
    base_kwargs = dict(cep="12345-678", city="São Paulo", district="Centro", street="Rua A", number="123")
    teste_construtor(lambda: Address(state=123, **base_kwargs), "Address com state=int (ERRO esperado)")
    teste_construtor(lambda: Address(state=12.5, **base_kwargs), "Address com state=float (ERRO esperado)")
    teste_construtor(lambda: Address(state='X', **base_kwargs), "Address com state=char (ERRO esperado)")
    teste_construtor(lambda: Address(state=object(), **base_kwargs), "Address com state=object (ERRO esperado)")
    teste_construtor(lambda: Address(state=None, **base_kwargs), "Address com state=None (ERRO esperado)")
    teste_construtor(lambda: Address(cep='12345-678', city="São Paulo", district="Centro", street="Rua A", number="123"), "Address sem state (omitido) (ERRO esperado)")
    teste_construtor(lambda: Address(state="", **base_kwargs), "Address com state vazio (ERRO esperado)")
    teste_construtor(lambda: Address(state="XX", **base_kwargs), "Address com state inexistente (sigla inválida) (ERRO esperado)")
    teste_construtor(lambda: Address(state="Sã", **base_kwargs), "Address com state inválido com caractere especial (ERRO esperado)")
    print("\n")

    # testes negativos - city
    base_kwargs = dict(cep="12345-678", state="SP", district="Centro", street="Rua A", number="123")
    teste_construtor(lambda: Address(city=123, **base_kwargs), "Address com city=int (ERRO esperado)")
    teste_construtor(lambda: Address(city=123.45, **base_kwargs), "Address com city=float (ERRO esperado)")
    teste_construtor(lambda: Address(city=object(), **base_kwargs), "Address com city=object (ERRO esperado)")
    teste_construtor(lambda: Address(city=None, **base_kwargs), "Address com city=None (ERRO esperado)")
    teste_construtor(lambda: Address(cep='12345-678', state="SP", district="Centro", street="Rua A", number="123"), "Address sem city (omitido) (ERRO esperado)")
    teste_construtor(lambda: Address(city="", **base_kwargs), "Address com city vazio (ERRO esperado)")
    print("\n")

    # testes negativos - district
    base_kwargs = dict(cep="12345-678", state="SP", city="São Paulo", street="Rua A", number="123")
    teste_construtor(lambda: Address(district=123, **base_kwargs), "Address com district=int (ERRO esperado)")
    teste_construtor(lambda: Address(district=12.3, **base_kwargs), "Address com district=float (ERRO esperado)")
    teste_construtor(lambda: Address(district=object(), **base_kwargs), "Address com district=object (ERRO esperado)")
    teste_construtor(lambda: Address(district=None, **base_kwargs), "Address com district=None (ERRO esperado)")
    teste_construtor(lambda: Address(cep='12345-678', state="SP", city="São Paulo", street="Rua A", number="123"), "Address sem district (omitido) (ERRO esperado)")
    teste_construtor(lambda: Address(district="", **base_kwargs), "Address com district vazio (ERRO esperado)")
    print("\n")

    # testes negativos - street
    base_kwargs = dict(cep="12345-678", state="SP", city="São Paulo", district="Centro", number="123")
    teste_construtor(lambda: Address(street=123, **base_kwargs), "Address com street=int (ERRO esperado)")
    teste_construtor(lambda: Address(street=12.3, **base_kwargs), "Address com street=float (ERRO esperado)")
    teste_construtor(lambda: Address(street=object(), **base_kwargs), "Address com street=object (ERRO esperado)")
    teste_construtor(lambda: Address(street=None, **base_kwargs), "Address com street=None (ERRO esperado)")
    teste_construtor(lambda: Address(cep='12345-678', state="SP", city="São Paulo", district="Centro", number="123"), "Address sem street (omitido) (ERRO esperado)")
    teste_construtor(lambda: Address(street="", **base_kwargs), "Address com street vazio (ERRO esperado)")
    print("\n")

    # testes negativos - number
    base_kwargs = dict(cep="12345-678", state="SP", city="São Paulo", district="Centro", street="Rua A")
    teste_construtor(lambda: Address(number=123, **base_kwargs), "Address com number=int (ERRO esperado)")
    teste_construtor(lambda: Address(number=12.3, **base_kwargs), "Address com number=float (ERRO esperado)")
    teste_construtor(lambda: Address(number='A', **base_kwargs), "Address com number=char (ERRO esperado)")
    teste_construtor(lambda: Address(number=object(), **base_kwargs), "Address com number=object (ERRO esperado)")
    teste_construtor(lambda: Address(number=None, **base_kwargs), "Address com number=None (ERRO esperado)")
    teste_construtor(lambda: Address(cep='12345-678', state="SP", city="São Paulo", district="Centro", street="Rua A"), "Address sem number (omitido) (ERRO esperado)")
    teste_construtor(lambda: Address(number="", **base_kwargs), "Address com number vazio (ERRO esperado)")
    print("\n")    

    # testes negativos - complement (atributo opcional)
    base_kwargs = dict(cep="12345-678", state="SP", city="São Paulo", district="Centro", street="Rua A", number="123")
    teste_construtor(lambda: Address(complement=123, **base_kwargs), "Address com complement=int (ERRO esperado)")
    teste_construtor(lambda: Address(complement=3.14, **base_kwargs), "Address com complement=float (ERRO esperado)")
    teste_construtor(lambda: Address(complement=object(), **base_kwargs), "Address com complement=object (ERRO esperado)")
    teste_construtor(lambda: Address(complement=None, **base_kwargs), "Address com complement=None (ERRO esperado)")
    print("\n")    


    # metodos
    print("\n Testes dos Métodos\n")
    if valid_address_min and valid_address_completo:
        # __str__
        teste_metodo(lambda: str(valid_address_min), "__str__() com address váido com dados mínimos (sem complement) (cep='12345-678' esperado)")
        teste_metodo(lambda: str(valid_address_completo), "__str__() com address váido com dados completos (com complement) (cep='87654-321' esperado)")
        print("\n")

        # to_dict()
        teste_metodo(lambda: valid_address_min.to_dict(), "to_dict() com address váido com dados mínimos (sem complement) (cep='12345-678' esperado)")
        teste_metodo(lambda: valid_address_completo.to_dict(), "to_dict() com address váido com dados completos (com complement) (cep='87654-321' esperado)")
        print("\n")

        # to_string_bank()
        teste_metodo(lambda: valid_address_min.to_string_bank(), "to_string_bank() com address váido com dados mínimos (sem complement) (cep='12345-678' esperado)")
        teste_metodo(lambda: valid_address_completo.to_string_bank(), "to_string_bank() com address váido com dados completos (com complement) (cep='87654-321' esperado)")
        print("\n")

        # validate_address() (positivos)
        teste_metodo(lambda: Address.validate_address(valid_address_min), "validate_address() com address váido com dados mínimos (sem complement) (OK esperado)")
        teste_metodo(lambda: Address.validate_address(valid_address_completo), "validate_address() com address válido com dados completos (com complement) (OK esperado)")

        # validate_address() (negativos)
        teste_metodo(lambda: Address.validate_address("str"), "validate_address() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: Address.validate_address(123), "validate_address() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: Address.validate_address(object()), "validate_address() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: Address.validate_address(None), "validate_address() com None (ERRO esperado)")
        teste_metodo(lambda: Address.validate_address(), "validate_address() sem argumento (ERRO esperado)")
        print("\n")

    # from_string()
    if valid_address_min and valid_address_completo:
        s1 = valid_address_min.to_string_bank()
        s2 = valid_address_completo.to_string_bank()

        #from string() (positivos)
        teste_metodo(lambda: Address.from_string(s1), "from_string() com address váido com dados mínimos (sem complement) (cep='12345-678' esperado)")
        teste_metodo(lambda: Address.from_string(s2), "from_string() com address váido com dados completos (com complement) (cep='87654-321' esperado)")

        # from_string() (negativos)
        teste_metodo(lambda: Address.from_string("texto plano"), "from_string() com tipo inválido string não JSON (ERRO esperado)")
        teste_metodo(lambda: Address.from_string(123), "from_string() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: Address.from_string(object()), "from_string() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: Address.from_string('{"estado":"SP"}'), "from_string() com dicionário incompleto (ERRO esperado)")
        teste_metodo(lambda: Address.from_string(("tuple",)), "from_string() com tipo inválido tupla (ERRO esperado)")
        teste_metodo(lambda: Address.from_string(["lista"]), "from_string() com tipo inválido lista (ERRO esperado)")
        teste_metodo(lambda: Address.from_string(None), "from_string() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: Address.from_string(), "from_string() sem argumento (ERRO esperado)")
        print("\n")