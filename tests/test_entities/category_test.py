#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_construtor, teste_metodo


def test_category():
    """teste da classe-entidade Category"""

    from entities.category import Category

    # testes de Category
    print("\n========================")
    print("Testes da classe Category")
    print("========================\n")

    #construtor
    print("\n Testes do Construtor\n")

    # teste positivo do construtor com id
    valid_category = teste_construtor(
    lambda: Category(name="Eletrônicos", id=1),
    "Category com name e id válidos"
    )

    # teste positivo do construtor sem id
    valid_category_no_id = teste_construtor(
    lambda: Category(name="Moda"),
    "Category com name válido e id omitido"
    )
    print("\n")

    # testes do construtor relacionados a atributos especificos
    # testes negativos do construtor - id
    teste_construtor(lambda: Category(name="Vestuário", id="um"), "Category com id=str")
    teste_construtor(lambda: Category(name="Vestuário", id=0), "Category com id=0")
    teste_construtor(lambda: Category(name="Vestuário", id=-10), "Category com id negativo")
    teste_construtor(lambda: Category(name="Vestuário", id=3.5), "Category com id=float")
    teste_construtor(lambda: Category(name="Vestuário", id=object()), "Category com id=object")
    print("\n")

    # testes negativos do construtor - name
    teste_construtor(lambda: Category(name=None, id=1), "Category com name=None")
    teste_construtor(lambda: Category(name=123, id=1), "Category com name=int")
    teste_construtor(lambda: Category(name=3.14, id=1), "Category com name=float")
    teste_construtor(lambda: Category(name=object(), id=1), "Category com name=object")
    teste_construtor(lambda: Category(name="", id=1), "Category com name vazio")
    teste_construtor(lambda: Category(id=1), "Category sem name (omitido)")
    print("\n")


    #metodos
    print("\n Testes dos Métodos\n")
    if valid_category and valid_category_no_id:
        # __str__
        teste_metodo(lambda: str(valid_category), "__str__() com id")
        teste_metodo(lambda: str(valid_category_no_id), "__str__() sem id")
        print("\n")

        # __eq__
        categoria_igual = Category(name="Eletrônicos", id=1)
        categoria_diferente = Category(name="Eletrônicos", id=2)
        categoria_sem_id = Category(name="Eletrônicos")

        teste_metodo(lambda: valid_category == categoria_igual, "__eq__() com id igual")
        teste_metodo(lambda: valid_category == categoria_diferente, "__eq__() com id diferente")
        teste_metodo(lambda: valid_category == categoria_sem_id, "__eq__() com um Category sem id")
        teste_metodo(lambda: valid_category == "não é Category", "__eq__() Category X string)")
        teste_metodo(lambda: valid_category == object(), "__eq__() Category X Object")
        teste_metodo(lambda: valid_category == None, "__eq__() Category X None")
        print("\n")

        # validate_category()
        teste_metodo(lambda: Category.validate_category(valid_category), "validate_category() com objeto Category válido com id")
        teste_metodo(lambda: Category.validate_category(valid_category_no_id), "validate_category() com objeto Category válido sem id")

        # validate_category() (negativos)
        teste_metodo(lambda: Category.validate_category("string"), "validate_category() com tipo inválido string")
        teste_metodo(lambda: Category.validate_category(123), "validate_category() com tipo inválido int")
        teste_metodo(lambda: Category.validate_category(object()), "validate_category() com tipo inválido objeto Object")
        teste_metodo(lambda: Category.validate_category(None), "validate_category() com tipo inválido None")
        teste_metodo(lambda: Category.validate_category(), "validate_category() sem argumento")
        print("\n")
