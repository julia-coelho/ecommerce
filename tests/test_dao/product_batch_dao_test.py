#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

from tests import teste_metodo_by_id_dao, get_cat, get_prod

def test_product_batch_dao(conexao):

    from dao.product_batch_dao import ProductBatchDAO
    from dao.product_dao import ProductDAO
    from dao.category_dao import CategoryDAO
    from entities import Date, Category, Product
    from entities.product_batch import ProductBatch

    print("\n==================================")
    print(" Testes da classe ProductBatchDAO ")
    print("==================================\n")

    dao = ProductBatchDAO(conexao)
    prod_dao = ProductDAO(conexao)
    cat_dao = CategoryDAO(conexao)

    # funções auxiliares

    def print_list_batches(filters):
        try:
            resultado = dao.list(**(filters))
            if not resultado:
                print("[OK] list() retornou lista vazia")
            else:
                print("\n------------------------------------------------------------------ LISTA DE LOTES DE PRODUTO ------------------------------------------------------------------")
                print("{:<10} {:<18} {:<20} {:<18} {:<15} {:<14} {:<17} {:<20} {:<10}".format(
                    "ID", "Lote", "Produto", "Marca", "Categoria", "Quantidade", "Fabricação", "Validade", "Vencido?"))
                print("-" * 160)
                for b in resultado:
                    id_, produto, marca, categoria, lote, quantidade, data_fab, data_val, vencido = b
                    vencido_str = "Fora da Validade" if vencido else "Dentro da Validade"
                    validade = data_val if data_val else "Indeterminada"
                    print(f"{id_:<5} {lote:<20} {produto:<20} {marca:<20} {categoria:<20} {quantidade:<10} {data_fab:<15} {validade:<18} {vencido_str:<10}")
                print("\n")
        except Exception as e:
            print(f"[ERRO Exception] list() -> {e}\n")

    # garantir produtos e categorias
    cat_dao.create_new(Category(name="Medicamentos"))
    cat_dao.create_new(Category(name="Cosmeticos"))

    cat_med = get_cat(conexao, 1)
    cat_cosm = get_cat(conexao, 2)

    prod_dao.create_new(Product("Paracetamol", "NeoQuimica", cat_med, 20.0))
    prod_dao.create_new(Product("Sabonete", "Palmolive", cat_cosm, 5.5))

    prod_paracetamol = get_prod(conexao, 1)
    prod_sabonete = get_prod(conexao, 2)

    # testes de create_new()
    print("\nTestes de create_new()")
    teste_metodo_by_id_dao(lambda: dao.create_new(ProductBatch(product=prod_paracetamol, batch_number="L1", manufacturing_date=Date(1, 1, 2023), quantity=100)), "create_new com lote válido com dados mínimos (sem data de validade) (novo lote #L1 do produto 'Paracetamol' da marca 'NeoQuimica' esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(ProductBatch(product=prod_sabonete, batch_number="L1", manufacturing_date=Date(1, 1, 2023), due_date=Date(1, 2, 2026), quantity=50)), "create_new com lote válido com dados completos (com data de validade) (novo lote #L2 do produto 'Sabonete' da marca 'Palmolive' esperado)")
    teste_metodo_by_id_dao(lambda: dao.create_new(ProductBatch(product=prod_paracetamol, batch_number="L1", manufacturing_date=Date(1, 1, 2023), quantity=100)), "create_new duplicado (ERRO esperado)")

    # testes de update_by_id()
    print("\nTestes de update_by_id()")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(1, ProductBatch(prod_paracetamol, batch_number="L1", manufacturing_date=Date(1, 1, 2023), quantity=80)), "update_by_id válido (Lote #L1 de produto 'Paracetamol', marca 'NeoQuimica' atualizado esperado)")
    teste_metodo_by_id_dao(lambda: dao.update_by_id(99, ProductBatch(product=prod_paracetamol, batch_number="L33", manufacturing_date=Date(1, 2, 1300), quantity=44)), "update_by_id com ID inexistente (ERRO esperado)")

    # testes de delete_by_id()
    print("\nTestes de delete_by_id()")
    teste_metodo_by_id_dao(lambda: dao.create_new(ProductBatch(product=prod_paracetamol, batch_number="TEMP", manufacturing_date=Date(1, 1, 2022), quantity=2)), "novo lote #TEMP do produto 'Paracetamol' da marca 'NeoQuimica'")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(3), "delete_by_id com dados (id) válido (delete de 'ID 3' esperado)")
    teste_metodo_by_id_dao(lambda: dao.delete_by_id(999), "delete_by_id inexistente (ERRO esperado)")

    # testes de find_by_id()
    print("\nTestes de find_by_id()")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(1), "find_by_id com dado (id) válido (lote 'L1' de 'Paracetamol', marca 'NeoQuimica' esperado)")
    teste_metodo_by_id_dao(lambda: dao.find_by_id(99), "find_by_id com ID inexistente (ERRO esperado)")

    # testes de list()
    print("\nTestes de list()")

    # cria lotes distintos para testes de list()
    dao.create_new(ProductBatch(product=prod_paracetamol, batch_number="PARA-VENCIDO", manufacturing_date=Date(1,1,2000), due_date=Date(1,1,2020), quantity=5))
    dao.create_new(ProductBatch(product=prod_paracetamol, batch_number="PARA-VALIDO", manufacturing_date=Date(1,1,2023), due_date=Date(1,1,2100), quantity=20))
    dao.create_new(ProductBatch(product=prod_sabonete, batch_number="SABONETE-1", manufacturing_date=Date(1,1,2024), due_date=Date(1,1,2025), quantity=3))
    dao.create_new(ProductBatch(product=prod_sabonete, batch_number="SABONETE-2", manufacturing_date=Date(1,6,2023), quantity=15))
    print("\nNovos lotes para popular tabela criados")

    i=1
    (filters) = dict()

    print(f"\n[{i}] list() sem filtros (lista populada esperada)")
    print_list_batches(filters)
    i+=1

    print(f"\n[{i}] list() com produto #1 (apenas os lotes do produto de ID 1 - produto 'Paracetamol' da marca 'NeoQuimica') (lista com 3 lotes esperada)")
    (filters) = dict(product_id=1)
    print_list_batches(filters)
    i+=1

    print(f"\n[{i}] list() com keyword 'SAB' (lista com 3 lotes esperada)")
    (filters) = dict(keyword="SAB")
    print_list_batches(filters)
    i+=1

    print(f"\n[{i}] list() com quantidade mínima 10 (lista populada esperada)")
    (filters) = dict(min_quantity=10)
    print_list_batches(filters)
    i+=1

    print(f"\n[{i}] list() com quantidade máxima 5 (lista populada esperada)")
    (filters) = dict(max_quantity=5)
    print_list_batches(filters)
    i+=1

    print(f"\n[{i}] list() por data de validade - apenas os vencidos")
    (filters) = dict(only_expired=True)
    print_list_batches(filters)
    i+=1

    print(f"\n[{i}] list() por data de validade - apenas os válidos")
    (filters) = dict(only_valid=True)
    print_list_batches(filters)
    i+=1


    print(f"\n[{i}] list() por data de validade - apenas os vencidos e apenas os válidos (ERRO esperado)")
    (filters) = dict(only_valid=True, only_expired=True)
    print_list_batches(filters)
    i+=1

    # ordenações
    for column in ["id", "product", "batch_number", "manufacturing_date", "due_date", "quantity"]:
        for direction in ["ASC", "DESC"]:
            print(f"\n[{i}] list() ordenada por {column} na direção {direction}")
            (filters) = dict(order_by_type=f'{column}', asc_or_desc=f'{direction}')
            print_list_batches(filters)
            i+=1

    print(f"\n[{i}] list() com ordenação por coluna inválida (lista ordenada por coluna id ASC esperada)")
    (filters) = dict(order_by_type='order')
    print_list_batches(filters)
    i+=1


    print(f"\n[{i}] list() com ordenação por direção inválida (lista ordenada por id em direção ascendente esperada)")
    (filters) = dict(asc_or_desc='crescente')
    print_list_batches(filters)
    i+=1


