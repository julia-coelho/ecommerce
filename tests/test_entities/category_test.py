#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo


def test_category():
    """teste da classe-entidade Category"""

    from entities.category import Category

    # testes de Category
    print("\n===========================")
    print(" Testes da classe Category ")
    print("===========================\n")

    #construtor
    print("\n Testes do Construtor\n")

    # testes positivos do construtor
    valid_category_min = teste_construtor(
    lambda: Category(name="Eletrônicos"),
    "Category válida com dados mínimos (sem id) (OK esperado)"
    )

    valid_category_max = teste_construtor(
    lambda: Category(name="Moda", id=2),
    "Category válida com dados completos (com id) (OK esperado)"
    )
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos - id (atributo opcional)
    teste_construtor(lambda: Category(name="Vestuário", id="um"), "Category com id=str (ERRO esperado)")
    teste_construtor(lambda: Category(name="Vestuário", id=0), "Category com id=0 (ERRO esperado)")
    teste_construtor(lambda: Category(name="Vestuário", id=-10), "Category com id negativo (ERRO esperado)")
    teste_construtor(lambda: Category(name="Vestuário", id=3.5), "Category com id=float (ERRO esperado)")
    teste_construtor(lambda: Category(name="Vestuário", id=object()), "Category com id=object (ERRO esperado)")
    print("\n")

    # testes negativos - name
    teste_construtor(lambda: Category(name=None, id=1), "Category com name=None (ERRO esperado)")
    teste_construtor(lambda: Category(name=123, id=1), "Category com name=int (ERRO esperado)")
    teste_construtor(lambda: Category(name=3.14, id=1), "Category com name=float (ERRO esperado)")
    teste_construtor(lambda: Category(name=object(), id=1), "Category com name=object (ERRO esperado)")
    teste_construtor(lambda: Category(name="", id=1), "Category com name vazio (ERRO esperado)")
    teste_construtor(lambda: Category(id=1), "Category sem name (omitido) (ERRO esperado)")
    print("\n")


    #metodos
    print("\n Testes dos Métodos\n")
    if valid_category_min and valid_category_max:
        # __str__
        teste_metodo(lambda: str(valid_category_min), "__str__() com Category válida com dados mínimos (sem id) (category com name='Eletrônicos', id=1, esperado)")
        teste_metodo(lambda: str(valid_category_max), "__str__() com Category válida com dados completos (com id) (category com name'Moda', id=2, esperado)")
        print("\n")

        # __eq__
        categoria_igual = Category(name="Eletrônicos", id=1)
        categoria_diferente = Category(name="Eletrônicos", id=2)
        categoria_sem_id = Category(name="Eletrônicos")

        teste_metodo(lambda: valid_category == categoria_igual, "__eq__() com id igual (True esperado)")
        teste_metodo(lambda: valid_category == categoria_diferente, "__eq__() com id diferente (False esperado)")
        teste_metodo(lambda: valid_category == categoria_sem_id, "__eq__() com um Category sem id (False esperado)")
        teste_metodo(lambda: valid_category == "não é Category", "__eq__() Category X string) (False esperado)")
        teste_metodo(lambda: valid_category == object(), "__eq__() Category X Object (False esperado)")
        teste_metodo(lambda: valid_category == None, "__eq__() Category X None (False esperado)")
        print("\n")

        # validate_category() (positivos)
        teste_metodo(lambda: Category.validate_category(valid_category), "validate_category() com date váido com dados mínimos (sem id) (category com name='Eletrônicos', id=1, esperado)")
        teste_metodo(lambda: Category.validate_category(valid_category_no_id), "validate_category() com Category válida com dados completos (com id) (category com name'Moda', id=2, esperado)")

        # validate_category() (negativos)
        teste_metodo(lambda: Category.validate_category("string"), "validate_category() com tipo inválido string (ERRO esperado)")
        teste_metodo(lambda: Category.validate_category(123), "validate_category() com tipo inválido int (ERRO esperado)")
        teste_metodo(lambda: Category.validate_category(object()), "validate_category() com tipo inválido objeto Object (ERRO esperado)")
        teste_metodo(lambda: Category.validate_category(None), "validate_category() com tipo inválido None (ERRO esperado)")
        teste_metodo(lambda: Category.validate_category(), "validate_category() sem argumento (ERRO esperado)")
        print("\n")
