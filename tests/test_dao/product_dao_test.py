# Aluna: Júlia Coelho Rodrigues
# RA: 22408388

from tests import teste_metodo_by_id_dao, get_cat, get_prod

def test_product_dao(conexao):

    from dao.category_dao import CategoryDAO
    from dao.product_dao import ProductDAO
    from dao.product_batch_dao import ProductBatchDAO
    from entities import Category, Product, Date
    from entities.product_batch import ProductBatch

    print("\n=============================")
    print(" Testes da classe ProductDAO ")
    print("=============================\n")

    cat_dao = CategoryDAO(conexao)
    prodbat_dao = ProductBatchDAO(conexao)
    dao = ProductDAO(conexao)

    # funções auxiliares

    def print_list_products(filters):
        try:
            resultado = dao.list(**filters)
            if not resultado:
                print("[OK] list() retornou lista vazia")
            else:
                print("\n----------------------------------------------------------------- LISTA DE PRODUTOS -----------------------------------------------------------------")
                print("{:<15} {:<25} {:<18} {:<14} {:<1} {:<5} {:<7} {:<13} {:<13} {:<13}".format("ID", "Nome", "Marca", "Categoria", "|", "Quantidade em Estoque", "|", "Preço", "Desconto", "Preço Final"))
                print("-" * 149)
                for p in resultado:
                    id_, nome, marca, cat_nome, preco, desc, preco_final, quantidade = p
                    vazio = ""
                    print(f"{id_:<5} {nome:<30} {marca:<22} {cat_nome:<15} | {vazio:<9} {quantidade:<11} | {vazio:<3} R$ {preco:<7.2f} - {vazio:<2} R$ {desc:<6.2f} = {vazio:<2} R$ {preco_final:<8.2f}")
                print("\n")
        except Exception as e:
            print(f"[ERRO Exception] list() -> {e}\n")

    # garantir categorias
    cat_dao.create_new(Category(name="Livros"))
    cat_dao.create_new(Category(name="Tecnologia"))

    cat_books = get_cat(conexao, 1)
    cat_tec = get_cat(conexao, 2)

    # testes de create_new()
    print("\nTestes de create_new()")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("Clean Code", "Uncle Bob", cat_books, 100.0)), "create_new com produto válido com dados mínimos (sem desconto unitário) (novo produto 'Clean Code' da marca 'Uncle Bob'' esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("Agile Software Development", "Uncle Bob", cat_books, 80.0, unit_discount=5.0)), "create_new com produto válido com dados completos (com desconto_unitario) (novo produto 'Agile Software Development' da marca 'Uncle Bob'' esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("", "Uncle Bob", cat_books, 50.0)), "create_new com nome vazio (ERRO esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("Clean Code", "", cat_books, 50.0)), "create_new com marca vazia (ERRO esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("Clean Code", "Uncle Bob", cat_books, 100.0)), "create_new duplicado (ERRO esperado)")

    # testes de update_by_id()
    print("\nTestes de update_by_id()")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(1, Product("Clean Code", "Robert C. Martin", cat_books, 110.0, unit_discount=15.0)), "update_by_id válido (marca atualizada para 'Robert C. Martin', dentre outras atualizações, esperado)")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(99, Product("Inexistente", "X", cat_books, 10.0)), "update_by_id com ID inexistente (ERRO esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("Clean Code", "Uncle Bob", cat_books, 100.0)), "novo produto 'Clean Code' da marca 'Uncle Bob' - possivel apenas porque o outro 'Clean Code' foi modificado para a marca 'Robert C. Martin' ")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(1, Product("Clean Code", "Uncle Bob", cat_books, 100.0)), "update_by_id com nome e marca de produto já sendo usados juntos na tabela (ERRO esperado)")

    # testes de delete_by_id()
    print("\nTestes de delete_by_id()")
    teste_metodo_by_id_dao(lambda: dao.create_new(Product("Produto Temporario", "Marca X", cat_tec, 25.0)), "novo produto 'Produto Temporario'")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(3), "delete_by_id com dados (id) válido (delete de 'ID 3' esperado)")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(999), "delete_by_id inexistente (ERRO esperado)")

    # testes de find_by_id()
    print("\nTestes de find_by_id()")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(1), "find_by_id com dado (id) válido (produto 'Clean Code', marca 'Robert C. Martin' esperado)")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(99), "find_by_id com ID inexistente (ERRO esperado)")

    # testes de outros metodos
    print("\n _get_table() testada indiretamente pelos testes de delete_by_id() e find_by_id()")
    print("\n _row_to_object() testada indiretamente pelos testes de find_by_id()")
    print("\n _row_to_full_object() de ProductDAO é igual a row_to_object(), já testado")
    print("\n find_by_id_full_object() de ProductDAO é igual a find_by_id(), já testada")

    # testes de list()
    print("\nTestes de list()")

    # cria produtos distintos para testes de list()
    dao.create_new(Product("The Pragmatic Programmer", "Andy Hunt", cat_books, 120.0, unit_discount=20.0))
    dao.create_new(Product("Estruturas de Dados", "Nivio Ziviani", cat_books, 85.0, unit_discount=5.0))
    dao.create_new(Product("Teclado Gamer", "Razer", cat_tec, 350.0, unit_discount=50.0))
    dao.create_new(Product("Mouse Sem Fio", "Logitech", cat_tec, 150.0, unit_discount=25.0))
    dao.create_new(Product("Tela 24 polegadas", "Logitech", cat_tec, 180.0, unit_discount=15.0))
    dao.create_new(Product("C++ Metaprogramming", "Machine L", cat_books, 130.0, unit_discount=10.0))
    dao.create_new(Product("Super Easy R", "James Hunter", cat_books, 150.0, unit_discount=15.0))

    prod_cleancode = get_prod(conexao, 1)

    prod_teclado = get_prod(conexao, 6)
    prod_mouse = get_prod(conexao, 7)
    prod_tela = get_prod(conexao, 8)

    # cria lotes distintos para testes de list()
    prodbat_dao.create_new(ProductBatch(prod_teclado, 'TEC1', Date(1, 8, 2024), 5))
    prodbat_dao.create_new(ProductBatch(prod_mouse, 'MOS3', Date(1, 1, 2024), 15))
    prodbat_dao.create_new(ProductBatch(prod_tela, 'TEL2', Date(1, 6, 2023), 2))
    prodbat_dao.create_new(ProductBatch(prod_cleancode, 'B123', Date(1, 6, 2002), 8))


    print("\nNovos produtos e lotes para popular tabelas criados")

    i=1
    filters = dict()

    print(f"\n[{i}] list() sem filtros (lista populada esperada)")
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com keyword='teclado' (lista com 1 produto esperada)")
    filters = dict(keyword='teclado')
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com category_id=2, 'Tecnologia' (lista com 4 produtos esperada)")
    filters = dict(category_id=2)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com category_id=2, 'Tecnologia', com min_quantity=1 (lista com 2 produtos esperada)")
    filters = dict(category_id=2, min_quantity=1)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com category_id=2, 'Tecnologia', com min_quantity=3 e max_quantity=20 (lista com 1 produto esperada)")
    filters = dict(category_id=2, min_quantity=3, max_quantity=20)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_product_amount=3 e max_product_amount=10, no_inventory=True (lista vazia esperada)")
    filters = dict(min_quantity=3, max_quantity=10, no_inventory=True)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com no_inventory=True (lista populada esperada)")
    filters = dict(no_inventory=True)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com only_inventory=True (lista populada esperada)")
    filters = dict(only_inventory=True)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com only_inventory=True e noinventory=True (ERRO esperado)")
    filters = dict(only_inventory=True, no_inventory=True)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_unit_price=100.0 (lista com 7 produtos esperada)")
    filters = dict(min_unit_price=100.0)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_unit_price=100.0 e max_unit_price=200.0 (lista com 6 produtos esperada)")
    filters = dict(min_unit_price=100.0, max_unit_price=200.0)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_unit_price=100.0, max_unit_price=200.0 e min_unit_discount=12.0 (lista com 5 produtos esperada)")
    filters = dict(min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0 e max_unit_discount=20.0 (lista com 4 produtos esperada)")
    filters = dict(min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0, max_unit_discount=20.0)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0, max_unit_discount=20.0 e min_final_unit_price=105.0 (lista com 2 produtos esperada)")
    filters = dict(min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0, max_unit_discount=20.0, min_final_unit_price=105.0)
    print_list_products(filters)
    i += 1

    print(f"\n[{i}] list() com min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0, max_unit_discount=20.0, min_final_unit_price=105.0 e max_final_unit_price=150.0 (lista com 1 produto esperada)")
    filters = dict(min_unit_price=100.0, max_unit_price=200.0, min_unit_discount=12.0, max_unit_discount=20.0, min_final_unit_price=105.0, max_final_unit_price=150.0)
    print_list_products(filters)
    i += 1

    # ordenações
    for column in ["id", "name", "brand", "category", "unit_price", "unit_discount", "final_unit_price", "quantity"]:
        for direction in ["ASC", "DESC"]:
            print(f"\n[{i}] list() ordenada por {column} na direção {direction}")
            filters = dict(order_by_type=f'{column}', asc_or_desc=f'{direction}')
            print_list_products(filters)
            i+=1

    print(f"\n[{i}] list() com ordenação por coluna inválida (lista ordenada por coluna id ASC esperada)")
    filters = dict(order_by_type='order')
    print_list_products(filters)
    i+=1


    print(f"\n[{i}] list() com ordenação por direção inválida (lista ordenada por id em direção ascendente esperada)")
    filters = dict(asc_or_desc='crescente')
    print_list_products(filters)
    i+=1