#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo


def test_date():
    """teste da classe-entidade Date"""

    from entities.date import Date

    print("\n========================")
    print("Testes da classe Date")
    print("========================\n")

    # construtor
    print("\n Testes do Construtor\n")

    # testes positivos do construtor
    valid_date_1 = teste_construtor(lambda: Date(1, 1, 2000), "Date(01/01/2000)")
    valid_date_2 = teste_construtor(lambda: Date(29, 2, 2020), "Date(29/02/2020 (ano bissexto)")
    valid_date_3 = teste_construtor(lambda: Date(31, 12, 1999), "Date(31/12/1999)")
    print("\n")

    # testes negativos do construtor - data invalida
    teste_construtor(lambda: Date(31, 2, 2021), "Date com dia inválido (31/02/2021)")
    teste_construtor(lambda: Date(0, 12, 2021), "Date com dia zero")
    teste_construtor(lambda: Date(15, 13, 2021), "Date com mês inválido (13)")
    print("\n")

    # testes negativos do construtor - tipos errados
    teste_construtor(lambda: Date(1.5, 1, 2000), "Date com day=float")
    teste_construtor(lambda: Date(1, 1.5, 2000), "Date com month=float")
    teste_construtor(lambda: Date(1, 1, 1.5), "Date com year=float")
    teste_construtor(lambda: Date("01", 1, 2000), "Date com day=str")
    teste_construtor(lambda: Date(1, "1", 2000), "Date com month=str")
    teste_construtor(lambda: Date(1, 1, "2000"), "Date com year=str")
    teste_construtor(lambda: Date(None, 1, 2000), "Date com day=None")
    teste_construtor(lambda: Date(1, None, 2000), "Date com month=None")
    teste_construtor(lambda: Date(1, 1, None), "Date com year=None")
    teste_construtor(lambda: Date(object(), 1, 2000), "Date com day=object")
    teste_construtor(lambda: Date(1, object(), 2000), "Date com month=object")
    teste_construtor(lambda: Date(1, 1, object()), "Date com year=object")
    teste_construtor(lambda: Date(1, 1, 1, 2000), "Date com 4 parametros (1 parametro a mais)")
    teste_construtor(lambda: Date(1, 2000), "Date com 2 parametros (1 parametro a menos)")
    teste_construtor(lambda: Date(), "Date vazia")
    print("\n")

    #metodos
    print("\n Testes dos Métodos\n")
    if valid_date_1 and valid_date_2:
        # __str__
        teste_metodo(lambda: str(valid_date_1), "__str__() com data 01/01/2000")
        teste_metodo(lambda: str(valid_date_2), "__str__() com data 29/02/2020")
        print("\n")

        # __eq__
        teste_metodo(lambda: valid_date_1 == Date(1, 1, 2000), "__eq__() com mesma data")
        teste_metodo(lambda: valid_date_1 == valid_date_2, "__eq__() com datas diferentes")
        teste_metodo(lambda: valid_date_1 == "01/01/2000", "__eq__() Date X string")
        teste_metodo(lambda: valid_date_1 == object(), "__eq__() Date X Object")
        teste_metodo(lambda: valid_date_1 == None, "__eq__() Date X None")
        print("\n")

        # to_date()
        teste_metodo(lambda: valid_date_1.to_date(), "to_date()")
        print("\n")

        # to_iso()
        teste_metodo(lambda: valid_date_1.to_iso(), "to_iso()")
        print("\n")

        # from_iso() (positivo)
        teste_metodo(lambda: Date.from_iso("1999-12-31"), "from_iso() com string ISO válida")

        # from_iso() (negativos)
        teste_metodo(lambda: Date.from_iso("ontem"), "from_iso() com string inválida")
        teste_metodo(lambda: Date.from_iso("01-01-2000"), "from_iso() com string fora do padrão ISO")
        teste_metodo(lambda: Date.from_iso(123), "from_iso() com tipo inválido int")
        teste_metodo(lambda: Date.from_iso(None), "from_iso() com tipo inválido None")
        teste_metodo(lambda: Date.from_iso(), "from_iso() sem argumento")
        print("\n")

        # validate_date() (positivo)
        teste_metodo(lambda: Date.validate_date(valid_date_1), "validate_date() com objeto válido Date")

        # validate_date() (negativos)
        teste_metodo(lambda: Date.validate_date("01/01/2000"), "validate_date() com tipo inválido string")
        teste_metodo(lambda: Date.validate_date(123), "validate_date() com tipo inválido int")
        teste_metodo(lambda: Date.validate_date(object()), "validate_date() com tipo inválido objeto Object")
        teste_metodo(lambda: Date.validate_date(None), "validate_date() com tipo inválido None")
        teste_metodo(lambda: Date.validate_date(), "validate_date() sem argumento")
        print("\n")

        # today()
        teste_metodo(lambda: Date.today(), "today()")
        print("\n")

        # datetime_today()
        teste_metodo(lambda: Date.datetime_today(), "datetime_today()")
        print("\n")
