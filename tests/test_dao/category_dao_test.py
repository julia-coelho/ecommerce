# Aluna: Júlia Coelho Rodrigues
# RA: 22408388

from tests import teste_metodo_by_id_dao, get_cat

def test_category_dao(conexao):

    from dao.category_dao import CategoryDAO
    from dao.product_dao import ProductDAO
    from entities.category import Category
    from entities.product import Product

    dao = CategoryDAO(conexao)

    print("\n==============================")
    print(" Testes da classe CategoryDAO ")
    print("==============================\n")

    # funcoes auxiliares

    def print_list_categories(filters):
        try:
            resultado = dao.list(**filters)
            if not resultado:
                print("[OK] list() retornou lista vazia")
            else:
                print("\n--------------- LISTA DE CATEGORIAS ---------------")
                print("{:<10} {:<20} {:<10}".format("ID", "Nome", "Qtd Produtos"))
                print("-" * 50)
                for categoria in resultado:
                    print("{:<7} {:<25} {:<10}".format(*categoria))
                print("\n")
        except Exception as e:
            print(f"[ERRO Exception] list() -> {e}\n")


    # testes de create_new
    print("\nTestes de create_new()")
    teste_metodo_by_id_dao(lambda: dao.create_new(Category(name="Esportes")), "create_new com nome válido (nova categoria 'Esportes' esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Category(name="")), "create_new com nome vazio (ERRO esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Category(name="Esportes")), "create_new com nome duplicado (ERRO esperado)")

    # testes de update_by_id
    print("\nTestes de update_by_id()")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(1, Category(name="Brinquedos")), "update_by_id(1) com dados válidos (nome atualizado para 'Brinquedos' esperado)")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(99, Category(name="Inexistente")), "update_by_id com ID inexistente (ERRO esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Category(name="Acessorios")), "nova categoria 'Acessorios'")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(1, Category(name="Acessorios")), "update_by_id com novo nome 'Acessorios' já existente na tabela (ERRO esperado)")

    # testes de delete_by_id
    print("\nTestes de delete_by_id()")
    teste_metodo_by_id_dao(lambda: dao.create_new(Category(name="Categoria Vazia")), "nova categoria 'Categoria Vazia'")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(3), "delete_by_id com dado (id) válido (delete de 'ID 3' esperado)")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(99), "delete_by_id com ID inexistente (ERRO esperado)")

    # testes de find_by_id()
    print("\nTestes de find_by_id()")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(1), "find_by_id com dado (id) válido (categoria 'Brinquedos' esperada)")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(99), "find_by_id com ID inexistente (ERRO esperado)")

    # testes de outros metodos
    print("\n _get_table() testada indiretamente pelos testes de delete_by_id() e find_by_id()")
    print("\n _row_to_object() testada indiretamente pelos testes de find_by_id()")
    print("\n _row_to_full_object() de CategoryDAO é igual a row_to_object(), já testado")
    print("\n find_by_id_full_object() de CategoryDAO é igual a find_by_id(), já testada")

    # testes de list()
    print("\nTestes de list()")

    # cria categorias para testar list()
    dao.create_new(Category(name="Bebidas"))
    dao.create_new(Category(name="Alimentos"))
    dao.create_new(Category(name="Limpeza"))
    dao.create_new(Category(name="Categoria Vazia"))
    dao.create_new(Category(name="Moveis"))

    # criar produtos em algumas categorias
    prod = ProductDAO(conexao)

    prod.create_new(Product("Agua Mineral", "Marca A", get_cat(conexao, 4), 2.5, unit_discount=0.0))
    prod.create_new(Product("Suco de Laranja", "Marca B", get_cat(conexao, 4), 5.0))
    prod.create_new(Product("Arroz", "Marca C", get_cat(conexao, 5), 4.8))
    prod.create_new(Product("Sabao em pó", "Marca D", get_cat(conexao, 6), 8.9))
    prod.create_new(Product("Sofa", "Marca E", get_cat(conexao, 8), 500))
    prod.create_new(Product("Detergente", "Marca F", get_cat(conexao, 6), 3.5))
    prod.create_new(Product("Leite", "Marca E", get_cat(conexao, 4), 8.0))

    print("\nNovas categorias e novos produtos para popular tabelas criados")

    i=1
    filters = dict()

    print(f"\n[{i}] list() sem filtros (lista populada esperada)")
    print_list_categories(filters)
    i += 1

    print(f"\n[{i}] list() com keyword=móveis (lista com única categoria 'Moveis' esperada)")
    filters = dict(keyword="móveis")
    print_list_categories(filters)
    i += 1

    print(f"\n[{i}] list() com min_product_amount=1 (lista populada esperada)")
    filters = dict(min_product_amount=1)
    print_list_categories(filters)
    i += 1

    print(f"\n[{i}] list() com min_product_amount=1 e max_product_amount=2 (lista com 3 categorias esperada)")
    filters = dict(min_product_amount=1, max_product_amount=2)
    print_list_categories(filters)
    i += 1

    print(f"\n[{i}] list() com min_product_amount=1 e max_product_amount=2, has_no_product=True (lista vazia esperada)")
    filters = dict(min_product_amount=1, max_product_amount=2, has_no_products=True)
    print_list_categories(filters)
    i += 1

    print(f"\n[{i}] list() com has_no_product=True (lista com 3 categorias esperada)")
    filters = dict(has_no_products=True)
    print_list_categories(filters)
    i += 1

    # ordenações
    for column in ["id", "name", "product_amount"]:
        for direction in ["ASC", "DESC"]:
            print(f"\n[{i}] list() ordenada por {column} na direção {direction}")
            filters = dict(order_by_type=f'{column}', asc_or_desc=f'{direction}')
            print_list_categories(filters)
            i+=1

    print(f"\n[{i}] list() com ordenação por coluna inválida (lista ordenada por coluna id ASC esperada)")
    filters = dict(order_by_type='order')
    print_list_categories(filters)
    i+=1


    print(f"\n[{i}] list() com ordenação por direção inválida (lista ordenada por id em direção ascendente esperada)")
    filters = dict(asc_or_desc='crescente')
    print_list_categories(filters)
    i+=1